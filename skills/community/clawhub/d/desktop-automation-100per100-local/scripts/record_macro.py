#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Macro Recorder GUI with Tkinter — Version ultra-robuste
Usage: python record_macro.py [output_path]

⚠️  PRIVACY WARNING: This recorder captures ALL keyboard events, including
passwords, credit card numbers, and other sensitive data. Use with extreme caution.
Only record macros for non-sensitive workflows. Never record while entering credentials.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import json, os, time, threading, logging, sys
from datetime import datetime
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key

# ============ CONFIGURATION LOGGING ============
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s — %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# ============ HANDLER TKINTER POUR LOGS ============
class TkinterLogHandler(logging.Handler):
    """Handler qui écrit dans un widget ScrolledText de Tkinter"""
    def __init__(self, text_widget, max_lines=100):
        super().__init__()
        self.text_widget = text_widget
        self.max_lines = max_lines
        self.setFormatter(logging.Formatter('%(asctime)s — %(levelname)s: %(message)s', '%H:%M:%S'))

    def emit(self, record):
        try:
            if self.text_widget is None:
                return
            msg = self.format(record)
            # Utiliser after_idle pour éviter de bloquer l'UI
            def append_log():
                self.text_widget.configure(state='normal')
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.configure(state='disabled')
                self.text_widget.yview(tk.END)
                # Limiter le nombre de lignes
                line_count = int(self.text_widget.index('end-1c').split('.')[0])
                if line_count > self.max_lines:
                    self.text_widget.delete(1.0, 2.0)
            self.text_widget.after_idle(append_log)
        except Exception:
            self.handleError(record)

# ============ MACRO RECORDER CLASS (Thread-safe) ============
class MacroRecorder:
    def __init__(self):
        self.recording = False
        self.events = []
        self.start_time = None
        self.output_path = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_window = None
        self.window_check_interval = 0.5
        self.window_thread = None
        self.stop_event = threading.Event()
        self.lock = threading.RLock()
        self.window_import_success = False
        
        # Debounce pour mousemove
        self.debounce_seconds = 1.0  # Timer par défaut
        self.pending_move = None  # Position en attente
        self.debounce_timer = None  # Timer thread
        self.debounce_lock = threading.Lock()  # Lock pour le debounce

    def _safe_import_pygetwindow(self):
        """Import pygetwindow de manière safe et cache le résultat"""
        if not self.window_import_success:
            try:
                import pygetwindow as gw
                self.gw = gw
                self.window_import_success = True
                return gw
            except ImportError as e:
                logger.error(f"Impossible d'importer pygetwindow : {e}")
                self.gw = None
                return None
        return self.gw

    def _append_event_safe(self, event):
        """Ajout thread-safe d'un événement"""
        with self.lock:
            self.events.append(event)

    def start(self, output_path):
        """Démarrer l'enregistrement avec validation"""
        # Validation du chemin de sortie
        if not output_path:
            raise ValueError("Chemin de sortie obligatoire")

        output_dir = os.path.dirname(output_path) or os.getcwd()
        if not os.path.isabs(output_dir):
            output_dir = os.path.abspath(output_dir)

        # Vérifier/create le dossier
        try:
            os.makedirs(output_dir, exist_ok=True)
            test_file = os.path.join(output_dir, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except Exception as e:
            raise IOError(f"Dossier de sortie inaccessible ({output_dir}) : {e}")

        # Reset state
        self.output_path = output_path
        self.recording = True
        self.events = []
        self.start_time = time.time()
        self.stop_event.clear()

        # Import pygetwindow une première fois
        self._safe_import_pygetwindow()

        # Start listeners avec gestion d'erreur
        try:
            self.mouse_listener = mouse.Listener(
                on_move=self._on_move_wrapper,
                on_click=self._on_click_wrapper,
                on_scroll=self._on_scroll_wrapper
            )
            self.keyboard_listener = keyboard.Listener(
                on_press=self._on_press_wrapper,
                on_release=self._on_release_wrapper
            )
            self.mouse_listener.start()
            self.keyboard_listener.start()
        except Exception as e:
            logger.error(f"Erreur démarrage listeners : {e}")
            self.stop()
            raise

        # Start window monitor thread
        self.window_thread = threading.Thread(target=self._window_monitor, daemon=True)
        self.window_thread.start()

        logger.info(f"Enregistrement démarré → {output_path}")

    def _window_monitor(self):
        """Surveillance de changement de fenêtre (thread séparé)"""
        last_title = None
        logger.debug("Window monitor thread démarré")
        while not self.stop_event.is_set():
            try:
                gw = self._safe_import_pygetwindow()
                if gw:
                    win = gw.getActiveWindow()
                    if win and win.title and win.title != last_title:
                        event = {
                            "timestamp": time.time() - self.start_time,
                            "action": "activate_window",
                            "params": {"title_substring": win.title}
                        }
                        self._append_event_safe(event)
                        last_title = win.title
                        logger.debug(f"Window change détectée : {win.title}")
            except Exception as e:
                logger.warning(f"Erreur dans window monitor (non bloquant) : {e}")
            time.sleep(self.window_check_interval)
        logger.debug("Window monitor thread arrêté")

    def _on_move_wrapper(self, x, y):
        """Gère le mouvement de souris avec debounce (1s par défaut)"""
        if not self.recording:
            return
        
        # Coordonnées arrondies
        x_int = int(round(x))
        y_int = int(round(y))
        
        with self.debounce_lock:
            # Annuler le timer précédent s'il existe
            if self.debounce_timer and self.debounce_timer.is_alive():
                self.debounce_timer.cancel()
            
            # Stocker la position actuelle
            self.pending_move = (x_int, y_int, time.time() - self.start_time)
            
            # Démarrer un nouveau timer
            self.debounce_timer = threading.Timer(self.debounce_seconds, self._flush_move)
            self.debounce_timer.daemon = True
            self.debounce_timer.start()
    
    def _flush_move(self):
        """Appelé après le debounce : enregistre la position finale"""
        with self.debounce_lock:
            if self.pending_move:
                x, y, timestamp = self.pending_move
                self._append_event_safe({
                    "timestamp": timestamp,
                    "action": "move_mouse",
                    "params": {"x": x, "y": y}
                })
                self.pending_move = None

    def _on_click_wrapper(self, x, y, button, pressed):
        if not self.recording or not pressed:
            return
        btn = 'left' if button == Button.left else 'right' if button == Button.right else 'middle'
        self._append_event_safe({
            "timestamp": time.time() - self.start_time,
            "action": "click",
            "params": {"x": int(round(x)), "y": int(round(y)), "button": btn}
        })

    def _on_scroll_wrapper(self, x, y, dx, dy):
        if not self.recording:
            return
        amount = int(dy * 120)  # Unités PyAutoGUI
        self._append_event_safe({
            "timestamp": time.time() - self.start_time,
            "action": "scroll",
            "params": {"amount": amount}
        })

    def _on_press_wrapper(self, key):
        if not self.recording:
            return
        try:
            k = key.char
        except AttributeError:
            k = str(key).replace('Key.', '')
        self._append_event_safe({
            "timestamp": time.time() - self.start_time,
            "action": "press_key",
            "params": {"key": k}
        })

    def _on_release_wrapper(self, key):
        # Pas enregistré pour l'instant
        pass

    def stop(self, timeout=5.0):
        """Arrêt propre avec attente des threads"""
        if not self.recording:
            return

        logger.info("Arrêt de l'enregistrement...")
        self.recording = False
        self.stop_event.set()

        # Annuler le timer de debounce s'il est en cours
        with self.debounce_lock:
            if self.debounce_timer and self.debounce_timer.is_alive():
                self.debounce_timer.cancel()
            # Vider le pending move si présent
            if self.pending_move:
                x, y, timestamp = self.pending_move
                self._append_event_safe({
                    "timestamp": timestamp,
                    "action": "move_mouse",
                    "params": {"x": x, "y": y}
                })
                self.pending_move = None

        # Arrêter les listeners
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

        # Attendre le thread window
        if self.window_thread and self.window_thread.is_alive():
            self.window_thread.join(timeout=timeout)
            if self.window_thread.is_alive():
                logger.warning("Window monitor thread toujours vivant après timeout")

        # Calcul duration
        duration = time.time() - self.start_time if self.start_time else 0
        logger.info(f"Enregistrement arrêté — {len(self.events)} événements, durée: {duration:.2f}s")

    def save(self):
        """Sauvegarde atomique des événements"""
        if not self.output_path:
            raise RuntimeError("Aucun chemin de sortie défini")

        # Préparer données
        meta = {
            "duration": time.time() - self.start_time if self.start_time else 0,
            "recorded_at": datetime.now().isoformat(),
            "event_count": len(self.events)
        }

        # Copie thread-safe des événements
        with self.lock:
            events_copy = list(self.events)

        data = {"meta": meta, "events": events_copy}

        # Écriture atomique
        temp_path = self.output_path + '.tmp'
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            # Renommage atomique (POSIX rename est atomique)
            os.replace(temp_path, self.output_path)
            logger.info(f"Macro sauvegardée : {self.output_path}")
            return self.output_path
        except Exception as e:
            # Nettoyage du fichier temporaire
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            raise IOError(f"Échec sauvegarde : {e}")

# ============ GUI TKINTER ============
class RecorderGUI:
    def __init__(self):
        self.recorder = MacroRecorder()
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'recorded_macro'))
        os.makedirs(self.output_dir, exist_ok=True)

        self.root = tk.Tk()
        self.root.title("Macro Recorder — Ultra Robuste")
        self.root.geometry("420x350")
        self.root.resizable(False, False)

        self.status_label = None
        self.start_button = None
        self.stop_button = None
        self.folder_label = None
        self.events_tree = None  # Treeview pour les événements
        self.debounce_var = None  # Variable Tkinter pour le debounce

        self._build_ui()

    def _build_ui(self):
        """Construction de l'interface"""
        pad = 10

        # Boutons principaux
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=pad)

        self.start_button = tk.Button(
            button_frame,
            text="🚀 Démarrer l'enregistrement",
            command=self._start_recording,
            width=30,
            bg='#4CAF50',
            fg='white',
            font=('Segoe UI', 10, 'bold')
        )
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(
            button_frame,
            text="🛑 Arrêter",
            command=self._stop_recording,
            width=30,
            bg='#f44336',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            state='disabled'
        )
        self.stop_button.pack(pady=5)

        tk.Button(
            button_frame,
            text="📁 Choisir dossier",
            command=self._choose_folder,
            width=30
        ).pack(pady=5)

        # Configuration du debounce
        debounce_frame = tk.Frame(self.root)
        debounce_frame.pack(pady=5)

        tk.Label(
            debounce_frame,
            text="Débounce mousemove (sec) :",
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT, padx=5)

        self.debounce_var = tk.StringVar(value="1.0")
        debounce_entry = tk.Entry(
            debounce_frame,
            textvariable=self.debounce_var,
            width=6,
            justify='center'
        )
        debounce_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            debounce_frame,
            text="Appliquer",
            command=self._apply_debounce,
            bg='#2196F3',
            fg='white',
            font=('Segoe UI', 9, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        # Dossier
        self.folder_label = tk.Label(
            self.root,
            text=self.output_dir,
            wraplength=350,
            fg='#666'
        )
        self.folder_label.pack(pady=5)

        # Statut
        self.status_label = tk.Label(
            self.root,
            text="✅ Prêt",
            fg='#2E7D32',
            font=('Segoe UI', 9)
        )
        self.status_label.pack(pady=5)

        # Zone de logs (légère, avec limitation automatique)
        log_frame = tk.LabelFrame(self.root, text="Logs en direct", padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            width=50,
            state='disabled',
            wrap=tk.WORD,
            font=('Consolas', 8)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Cadre pour les événements enregistrés (affichage temps réel)
        events_frame = tk.LabelFrame(self.root, text="Événements enregistrés (temps réel)", padx=5, pady=5)
        events_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview pour afficher les événements
        self.events_tree = ttk.Treeview(
            events_frame,
            columns=("temps", "action", "details"),
            show='headings',
            height=6
        )
        self.events_tree.heading("temps", text="Temps (s)")
        self.events_tree.heading("action", text="Action")
        self.events_tree.heading("details", text="Détails")
        self.events_tree.column("temps", width=60, minwidth=50)
        self.events_tree.column("action", width=80, minwidth=70)
        self.events_tree.column("details", width=200, minwidth=150)

        # Scrollbar pour le Treeview
        events_scroll = ttk.Scrollbar(events_frame, orient=tk.VERTICAL, command=self.events_tree.yview)
        self.events_tree.configure(yscrollcommand=events_scroll.set)

        self.events_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        events_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Info label
        tk.Label(
            self.root,
            text="⚠️  PRIVACY: records ALL keystrokes (including passwords). Use with caution.",
            wraplength=350,
            fg='#D32F2F',
            font=('Segoe UI', 8, 'bold')
        ).pack(pady=5)

        tk.Label(
            self.root,
            text="Enregistre : souris, clic, défilement, clavier, changements de fenêtre",
            wraplength=350,
            fg='#666',
            font=('Segoe UI', 8)
        ).pack(pady=5)

        # Attacher le handler de logging
        self._attach_log_handler()

    def _attach_log_handler(self):
        """Attache le handler Tkinter au logger pour afficher les logs dans l'UI"""
        handler = TkinterLogHandler(self.log_text, max_lines=100)
        logger.addHandler(handler)

    def _update_events_list(self):
        """Met à jour la liste des événements enregistrés en temps réel"""
        if self.events_tree is None:
            return
        
        # Effacer les anciennes entrées
        self.events_tree.delete(*self.events_tree.get_children())
        
        # Copie thread-safe des événements
        with self.recorder.lock:
            events = list(self.recorder.events)
        
        # Afficher les 100 derniers événements
        for event in events[-100:]:
            t = event.get('timestamp', 0)
            action = event.get('action', '?')
            params = event.get('params', {})
            
            # Formater les détails selon l'action
            if action == 'click':
                details = f"({params.get('x')},{params.get('y')}) [{params.get('button')}]"
            elif action == 'press_key':
                details = f"'{params.get('key')}'"
            elif action == 'type':
                text = params.get('text', '')
                details = f"'{text[:30]}{'...' if len(text)>30 else ''}'"
            elif action == 'move_mouse':
                details = f"({params.get('x')},{params.get('y')})"
            elif action == 'scroll':
                details = f"{params.get('amount')}"
            elif action == 'drag':
                start = params.get('start', (0,0))
                end = params.get('end', (0,0))
                details = f"({start})→({end})"
            elif action == 'activate_window':
                title = params.get('title_substring', '')
                details = f"'{title[:30]}{'...' if len(title)>30 else ''}'"
            else:
                details = str(params)[:40]
            
            self.events_tree.insert("", tk.END, values=(f"{t:.3f}", action, details))
        
        # Programmer la prochaine mise à jour si enregistrement en cours
        if self.recorder.recording:
            self.root.after(250, self._update_events_list)

    def _start_recording(self):
        """Callback bouton Démarrer"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"macro_{timestamp}.json"
            full_path = os.path.join(self.output_dir, filename)

            self.recorder.start(full_path)
            self.status_label.config(text="🔴 Enregistrement en cours...", fg='#D32F2F')
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            # Démarrer l'affichage des événements en temps réel
            self._update_events_list()
        except Exception as e:
            logger.error(f"Échec démarrage : {e}")
            messagebox.showerror("Erreur", f"Impossible de démarrer : {e}")

    def _stop_recording(self):
        """Callback bouton Arrêter"""
        try:
            self.recorder.stop()
            saved_path = self.recorder.save()
            messagebox.showinfo("✅ Enregistrement terminé", f"Macro sauvegardée :\n{saved_path}")
            self.status_label.config(text="✅ Prêt", fg='#2E7D32')
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
        except Exception as e:
            logger.error(f"Échec arrêt/sauvegarde : {e}")
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")
            self.status_label.config(text="❌ Erreur", fg='#C62828')
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')

    def _choose_folder(self):
        """Choix du dossier de sortie"""
        folder = filedialog.askdirectory(initialdir=self.output_dir)
        if folder:
            self.output_dir = folder
            self.folder_label.config(text=folder)

    def _apply_debounce(self):
        """Applique le paramètre de debounce depuis l'Entry"""
        try:
            value = float(self.debounce_var.get())
            if value < 0.1 or value > 10.0:
                raise ValueError("Entre 0.1 et 10 secondes")
            self.recorder.debounce_seconds = value
            logger.info(f"Débounce configuré à {value}s")
        except ValueError as e:
            messagebox.showerror("Valeur invalide", f"Le debounce doit être un nombre entre 0.1 et 10 secondes.\nErreur: {e}")

    def run(self):
        """Lancement de la boucle Tkinter"""
        self.root.mainloop()

# ============ POINT D'ENTRÉE ============
if __name__ == '__main__':
    try:
        app = RecorderGUI()
        app.run()
    except Exception as e:
        logger.critical(f"Erreur fatale : {e}")
        messagebox.showerror("Erreur fatale", str(e))
        sys.exit(1)
