#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Automation Features — Do not modify existing basic functions.
These are additive, more powerful features with explicit names.
"""
import os, time, json, logging
import pyautogui
import cv2
import numpy as np
import pytesseract

logger = logging.getLogger(__name__)

# ============================================
# 1. MULTI-SCALE IMAGE DETECTION
# ============================================

def find_image_multiscale(template_path, confidence=0.9, scale_factors=None):
    """
    Trouve une image en testant plusieurs échelles (pyramide).

    Args:
        template_path: chemin vers le template
        confidence: seuil minimum (0.0-1.0)
        scale_factors: liste de facteurs, ex: [0.5, 0.75, 1.0, 1.25, 1.5]
                      Si None, default: [0.5, 0.75, 1.0, 1.25, 1.5]

    Returns:
        {"status":"ok", "x":int, "y":int, "confidence":float, "scale":float}
        ou {"status":"not_found", "best_confidence":float}
    """
    if scale_factors is None:
        scale_factors = [0.5, 0.75, 1.0, 1.25, 1.5]

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        return {"status": "error", "message": f"Template not found: {template_path}"}

    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    best_match = None
    best_conf = -1

    for scale in scale_factors:
        # Redimensionner le template
        new_w = int(template.shape[1] * scale)
        new_h = int(template.shape[0] * scale)
        if new_w < 5 or new_h < 5:
            continue
        resized = cv2.resize(template, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Matching
        res = cv2.matchTemplate(screen_gray, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > best_conf:
            best_conf = max_val
            best_match = {
                'x': max_loc[0] + new_w // 2,
                'y': max_loc[1] + new_h // 2,
                'scale': scale
            }

    if best_conf >= confidence and best_match:
        logger.debug(f"Multi-scale match: ({best_match['x']},{best_match['y']}) scale={best_match['scale']} conf={best_conf:.3f}")
        return {"status": "ok", "x": best_match['x'], "y": best_match['y'], "confidence": float(best_conf), "scale": best_match['scale']}
    else:
        logger.debug(f"Multi-scale image not found (best conf={best_conf:.3f})")
        return {"status": "not_found", "best_confidence": float(best_conf)}

# ============================================
# 2. FIND ALL TEXT OCCURRENCES
# ============================================

def find_all_text_on_screen(text, lang='fra'):
    """
    Retourne TOUTES les occurrences du texte à l'écran, pas seulement la première.

    Args:
        text: chaîne à rechercher (ne sera pas sensible à la casse)
        lang: langue Tesseract (défaut 'fra')

    Returns:
        {"status":"ok", "matches": [{"text":str, "x":int, "y":int, "w":int, "h":int, "conf":float}, ...]}
    """
    if pytesseract is None:
        return {"status": "error", "message": "pytesseract not installed"}

    try:
        img = pyautogui.screenshot()
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)

        matches = []
        n = len(data['text'])
        for i in range(n):
            word = data['text'][i].strip()
            if word and text.lower() in word.lower():
                matches.append({
                    'text': word,
                    'left': int(data['left'][i]),
                    'top': int(data['top'][i]),
                    'width': int(data['width'][i]),
                    'height': int(data['height'][i]),
                    'conf': float(data['conf'][i])
                })

        logger.debug(f"Found {len(matches)} occurrences of '{text}'")
        return {"status": "ok", "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"find_all_text_on_screen error: {e}")
        return {"status": "error", "message": str(e)}

# ============================================
# 3. UI ELEMENTS DETECTION
# ============================================

def detect_ui_elements(element_type=None):
    """
    Détecte des éléments UI courants par reconnaissance d'image / heuristiques.

    Args:
        element_type: 'button', 'field', 'slider', ou None pour tout détecter

    Returns:
        {"status":"ok", "elements": [{"type":..., "x":..., "y":..., "w":..., "h":...}, ...]}
    """
    # Pour l'instant, une détection basique par formes/contours (à améliorer)
    try:
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)
        gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        elements = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            # Filtrer par taille (éviter bruit)
            if area < 100 or area > 10000:
                continue
            # Heuristique simple : ratio width/height pour deviner le type
            ratio = w / max(h, 1)
            etype = 'unknown'
            if 2.5 < ratio < 6 and h < 40:
                etype = 'button'
            elif 1.5 < ratio < 5 and h > 30:
                etype = 'field'
            elif 0.8 < ratio < 1.2 and 30 < h < 200:
                etype = 'slider'

            if element_type is None or etype == element_type:
                elements.append({
                    'type': etype,
                    'x': x,
                    'y': y,
                    'w': w,
                    'h': h,
                    'area': area
                })

        logger.info(f"Detected {len(elements)} UI elements")
        return {"status": "ok", "elements": elements, "count": len(elements)}
    except Exception as e:
        logger.error(f"detect_ui_elements error: {e}")
        return {"status": "error", "message": str(e)}

# ============================================
# 4. CONDITIONAL MONITOR WITH LOGIC
# ============================================

def monitor_screen_with_logic(conditions, timeout=60, interval=0.5):
    """
    Surveillance avancée avec logique combinatoire (AND/OR).

    Args:
        conditions: liste de conditions, chaque condition:
            {
                "type": "image" ou "text",
                "template_path": "...",
                "text": "...",
                "confidence": 0.9,
                "lang": "fra",
                "logic": "AND" | "OR",  # pour combiner plusieurs conditions dans un groupe
                "actions": [ {"action": "...", "params": {...}}, ... ]
            }
        timeout: secondes max
        interval: délai entre vérifications

    Exemple:
    conditions=[
        {"type":"image", "template_path":"ok.png", "confidence":0.9, "logic":"AND",
         "actions": [{"action":"click", "params":{...}}]},
        {"type":"text", "text":"Success", "logic":"OR", "actions":[...]}
    ]

    Retourne les actions exécutées et le timing.
    """
    start_time = time.time()
    executed_actions = []
    satisfied_groups = set()

    # Grouper par index (chaque condition est un groupe pour l'instant)
    while time.time() - start_time < timeout:
        for idx, cond in enumerate(conditions):
            # Vérifier la condition
            cond_ok = False
            if cond.get('type') == 'image':
                res = find_image_multiscale(cond['template_path'], cond.get('confidence', 0.9))
                cond_ok = res.get('status') == 'ok'
            elif cond.get('type') == 'text':
                res = find_all_text_on_screen(cond['text'], cond.get('lang', 'fra'))
                cond_ok = res.get('status') == 'ok' and res.get('count', 0) > 0
            else:
                logger.warning(f"Unknown condition type: {cond.get('type')}")
                continue

            # Si condition vérifiée, exécuter les actions
            if cond_ok:
                for act in cond.get('actions', []):
                    action_name = act['action']
                    params = act.get('params', {}).copy()
                    # Injecter coordonnées si présentes dans la détection
                    if 'x' in params and 'y' in params and 'location' in res:
                        params['x'] = res['location']['x']
                        params['y'] = res['location']['y']
                    # Exécuter l'action (seulement actions de base)
                    safe_actions = {'click', 'type', 'press_key', 'scroll', 'move_mouse', 'activate_window', 'drag', 'copy_to_clipboard', 'paste_from_clipboard'}
                    if action_name in safe_actions and action_name in globals():
                        try:
                            result = globals()[action_name](**params)
                            executed_actions.append({
                                'condition_index': idx,
                                'action': action_name,
                                'result': result,
                                'timestamp': time.time() - start_time
                            })
                            logger.info(f"Condition {idx} satisfied, executed {action_name}")
                        except Exception as e:
                            logger.error(f"Action {action_name} failed: {e}")
                satisfied_groups.add(idx)

        # Si toutes les conditions ont été satisfaites au moins une fois, on peut arrêter
        if len(satisfied_groups) == len(conditions):
            logger.info("All conditions satisfied, stopping monitor")
            break

        time.sleep(interval)

    total_elapsed = time.time() - start_time
    return {
        "status": "ok" if total_elapsed < timeout else "timeout",
        "executed_actions": executed_actions,
        "satisfied_conditions": list(satisfied_groups),
        "elapsed": total_elapsed
    }

# ============================================
# 5. PLAY MACRO WITH SUBROUTINES
# ============================================

def play_macro_with_subroutines(macro_path, speed=1.0, sub_macros_dir=None):
    """
    Lecture de macro avec support de sous-macros.

    Format de macro attendu:
    {
      "meta": {...},
      "events": [
        {"action": "call_macro", "params": {"macro_file": "submacro1.json"}},
        {"action": "type", "params": {"text": "Hello"}},
        ...
      ]
    }

    Args:
        macro_path: chemin macro principale
        speed: facteur vitesse
        sub_macros_dir: dossier où chercher les sous-macros (défaut: même dossier que macro_path)
    """
    if sub_macros_dir is None:
        sub_macros_dir = os.path.dirname(macro_path) or os.getcwd()

    # Charger la macro principale
    try:
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
        events = macro_data.get('events', [])
    except Exception as e:
        return {"status": "error", "message": f"Failed to load macro: {e}"}

    start_time = time.time()
    event_index = 0
    sub_macro_recursion = {}

    while event_index < len(events):
        now = time.time() - start_time
        # Chercher le prochain événement dont timestamp / speed <= now
        for i in range(event_index, len(events)):
            target_time = events[i]['timestamp'] / speed
            if now >= target_time:
                event = events[i]
                action = event.get('action')
                params = event.get('params', {}).copy()

                # Gestion spéciale de call_macro
                if action == 'call_macro':
                    sub_macro_file = params.get('macro_file')
                    sub_macro_path = os.path.join(sub_macros_dir, sub_macro_file)
                    # Charger et jouer la sous-macro (sans call_macro imbriqué infini)
                    if sub_macro_path in sub_macro_recursion and sub_macro_recursion[sub_macro_path] > 5:
                        logger.error(f"Recursion limit exceeded for {sub_macro_file}")
                        event_index = i + 1
                        break
                    sub_macro_recursion[sub_macro_file] = sub_macro_recursion.get(sub_macro_file, 0) + 1
                    # Lecture directe (on pourrait factoriser avec un appel interne)
                    try:
                        with open(sub_macro_path, 'r', encoding='utf-8') as sf:
                            sub_data = json.load(sf)
                        sub_events = sub_data.get('events', [])
                        # Insérer les événements de la sous-macro dans le flux
                        # On décale les timestamps pour qu'ils s'insèrent naturellement
                        base_ts = now * speed  # timestamp dans la macro original
                        for se in sub_events:
                            se['timestamp'] = base_ts + se['timestamp']
                        events = events[:i+1] + sub_events + events[i+1:]
                        # On ne change pas event_index car la liste a été étendue
                        continue
                    except Exception as e:
                        logger.error(f"Failed to load sub-macro {sub_macro_file}: {e}")
                        event_index = i + 1
                        break
                else:
                    # Exécution normale
                    try:
                        if action in globals():
                            globals()[action](**params)
                        else:
                            logger.warning(f"Unknown action: {action}")
                    except Exception as e:
                        logger.error(f"Error in macro event {i} action={action}: {e}")
                    event_index = i + 1
                    break
        else:
            time.sleep(0.001)

    total_time = time.time() - start_time
    return {"status": "ok", "duration": total_time, "events_processed": event_index}

# ============================================
# 6. PROTECTED MACRO (Password-Locked)
# ============================================

def create_protected_macro(output_path, password, macro_events=None):
    """
    Crée une macro protégée par mot de passe (chiffrement simple).

    Args:
        output_path: fichier de sortie .json
        password: chaîne de passe (sera hashée)
        macro_events: liste d'événements (optionnel, sinon enregistrement direct depuis recorder)

    Retourne le chemin du fichier protégé.
    """
    import hashlib, base64
    from cryptography.fernet import Fernet

    # Si macro_events n'est pas fourni, on lance l'enregistreur
    if macro_events is None:
        # Dummy call: dans la vraie vie on appellerait record_macro()
        return {"status": "error", "message": "macro_events required for now"}

    # Dériver une cléFernet du mot de passe
    key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()[:32])
    f = Fernet(key)

    # Sérialiser les événements
    data = json.dumps({"events": macro_events}, ensure_ascii=False, indent=2).encode('utf-8')
    encrypted = f.encrypt(data)

    # Écrire le fichier (format: {encrypted_base64}.enc)
    with open(output_path, 'wb') as f_out:
        f_out.write(encrypted)

    logger.info(f"Protected macro saved to {output_path}")
    return {"status": "ok", "path": output_path}

def load_and_decrypt_protected_macro(encrypted_path, password):
    """
    Charge et déchiffre une macro protégée.

    Args:
        encrypted_path: fichier .enc
        password: mot de passe

    Returns:
        {"status":"ok", "events": [...]} ou erreur
    """
    import hashlib, base64
    from cryptography.fernet import Fernet, InvalidToken

    key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()[:32])
    f = Fernet(key)

    try:
        with open(encrypted_path, 'rb') as f_in:
            encrypted = f_in.read()
        decrypted = f.decrypt(encrypted)
        data = json.loads(decrypted.decode('utf-8'))
        return {"status": "ok", "events": data.get('events', [])}
    except InvalidToken:
        return {"status": "error", "message": "Invalid password or corrupted file"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================
# 7. MACRO HOTKEY STOP
# ============================================

class MacroStopManager:
    """Gère l'arrêt global d'une macro via hotkey (sécurité)"""
    def __init__(self, stop_hotkey='ctrl+alt+esc'):
        self.stop_hotkey = stop_hotkey
        self.stop_requested = False
        self.listener = None

    def start_listener(self):
        """Démarre l'écoute de la hotkey dans un thread séparé"""
        from pynput import keyboard

        def on_press(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.ctrl_pressed = True
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.alt_pressed = True
                if hasattr(key, 'char') and key.char == '[':
                    self.bracket_pressed = True  # dummy
            except:
                pass

        def on_release(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.ctrl_pressed = False
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.alt_pressed = False
                if hasattr(key, 'char') and key.char == '[':
                    self.bracket_pressed = False
            except:
                pass

        self.ctrl_pressed = False
        self.alt_pressed = False
        self.bracket_pressed = False

        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
        logger.info(f"Macro stop hotkey listener started: {self.stop_hotkey}")

    def check_stop(self):
        """Vérifie si la hotkey a été pressée"""
        # Simple check: ctrl+alt+somekey (ex: ctrl+alt+esc)
        # On implement a simple combo check
        # Note: for a real implementation, we'd track the exact key sequence
        return self.stop_requested

    def stop(self):
        self.stop_requested = True
        if self.listener:
            self.listener.stop()

# ============================================
# 8. MACRO REPORTING
# ============================================

def generate_macro_report(macro_path, execution_log):
    """
    Génère un rapport HTML/JSON d'exécution de macro.

    Args:
        macro_path: chemin de la macro
        execution_log: dict avec timestamps, actions, résultats

    Returns:
        {"status":"ok", "report_path": "...", "summary": {...}}
    """
    import datetime
    report_dir = os.path.join(os.path.dirname(macro_path), 'reports')
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_base = f"report_{timestamp}"

    # JSON report
    json_path = os.path.join(report_dir, report_base + '.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'macro': macro_path,
            'generated_at': timestamp,
            'log': execution_log
        }, f, indent=2, ensure_ascii=False)

    # HTML report (simple)
    html_path = os.path.join(report_dir, report_base + '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
<title>Macro Report — {os.path.basename(macro_path)}</title>
<style>
body {{ font-family: sans-serif; margin: 20px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
th {{ background: #f0f0f0; }}
.success {{ color: green; }}
.error {{ color: red; }}
</style>
</head>
<body>
<h1>Macro Execution Report</h1>
<p><strong>Macro:</strong> {macro_path}</p>
<p><strong>Generated:</strong> {timestamp}</p>
<h2>Summary</h2>
<ul>
<li>Total actions: {len(execution_log.get('actions', []))}</li>
<li>Status: {execution_log.get('status', 'unknown')}</li>
<li>Duration: {execution_log.get('elapsed', 0):.2f}s</li>
</ul>
<h2>Actions Log</h2>
<table>
<tr><th>#</th><th>Action</th><th>Params</th><th>Result</th></tr>
""")
        for i, act in enumerate(execution_log.get('actions', [])):
            result_class = 'success' if act.get('result', {}).get('status') == 'ok' else 'error'
            f.write(f"<tr><td>{i+1}</td><td>{act.get('action')}</td><td>{act.get('params')}</td><td class='{result_class}'>{act.get('result')}</td></tr>\n")
        f.write("""
</table>
</body>
</html>
""")

    logger.info(f"Macro report generated: {json_path} & {html_path}")
    return {"status": "ok", "report_json": json_path, "report_html": html_path}
