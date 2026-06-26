#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Macro Player — Version ultra-robuste
Usage: python play_macro.py <macro_json_path> [speed_factor]
"""
import sys, json, time, os, logging
import pyautogui
import pygetwindow as gw

# ============ CONFIGURATION LOGGING ============
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s — %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# ============ VALIDATION ET PRÉPARATION ============
def validate_macro_file(path):
    """Validation exhaustive du fichier macro"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    if not os.path.isfile(path):
        raise ValueError(f"Ce n'est pas un fichier : {path}")

    try:
        size = os.path.getsize(path)
        if size == 0:
            raise ValueError("Fichier vide")
    except Exception as e:
        raise IOError(f"Impossible de lire le fichier : {e}")

    return True

def load_macro(path):
    """Chargement sécurisé du fichier JSON"""
    validate_macro_file(path)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide : {e} (ligne {e.lineno}, colonne {e.colno})")
    except UnicodeDecodeError as e:
        raise ValueError(f"Erreur d'encodage (doit être UTF-8) : {e}")
    except Exception as e:
        raise IOError(f"Erreur lecture fichier : {e}")

    # Validation de la structure minimale
    if not isinstance(data, dict):
        raise ValueError("Macro invalide : racine doit être un objet JSON")

    if 'events' not in data:
        raise ValueError("Macro invalide : champ 'events' manquant")

    if not isinstance(data['events'], list):
        raise ValueError("Macro invalide : 'events' doit être un tableau")

    # Vérifier chaque événement
    for i, event in enumerate(data['events']):
        if not isinstance(event, dict):
            raise ValueError(f"Événement {i}: doit être un objet")

        if 'action' not in event:
            raise ValueError(f"Événement {i}: champ 'action' manquant")

        if 'timestamp' not in event:
            raise ValueError(f"Événement {i}: champ 'timestamp' manquant")

        if 'params' not in event:
            raise ValueError(f"Événement {i}: champ 'params' manquant")

    logger.info(f"Macro chargée : {len(data['events'])} événements")
    return data

# ============ EXÉCUTION DES ACTIONS ============
def execute_action(action, params, dry_run=False):
    """Exécution robuste d'une action avec fallbacks"""
    try:
        if action == 'click':
            x = params['x']
            y = params['y']
            button = params.get('button', 'left')
            if not dry_run:
                pyautogui.click(x=x, y=y, button=button)
            logger.debug(f"Click: ({x},{y}) button={button}")

        elif action == 'move_mouse':
            x = params['x']
            y = params['y']
            if not dry_run:
                pyautogui.moveTo(x, y)
            logger.debug(f"Move: ({x},{y})")

        elif action == 'press_key':
            key = params['key']
            if not dry_run:
                pyautogui.press(key)
            logger.debug(f"Press key: {key}")

        elif action == 'scroll':
            amount = params['amount']
            if not dry_run:
                pyautogui.scroll(amount)
            logger.debug(f"Scroll: {amount}")

        elif action == 'type':
            text = params['text']
            interval = params.get('interval', 0.0)
            if not dry_run:
                pyautogui.typewrite(text, interval=interval)
            logger.debug(f"Type: '{text}' interval={interval}")

        elif action == 'activate_window':
            title_sub = params['title_substring']
            wins = gw.getWindowsWithTitle(title_sub)
            if wins:
                if not dry_run:
                    wins[0].activate()
                logger.debug(f"Activate window: {title_sub}")
            else:
                logger.warning(f"Fenêtre non trouvée : '{title_sub}'")

        elif action == 'drag':
            start_x = params['start_x']
            start_y = params['start_y']
            end_x = params['end_x']
            end_y = params['end_y']
            duration = params.get('duration', 0.5)
            button = params.get('button', 'left')
            if not dry_run:
                pyautogui.moveTo(start_x, start_y)
                pyautogui.dragTo(end_x, end_y, duration=duration, button=button)
            logger.debug(f"Drag: ({start_x},{start_y})→({end_x},{end_y})")

        elif action == 'copy_to_clipboard':
            text = params['text']
            try:
                import pyperclip
                if not dry_run:
                    pyperclip.copy(text)
                logger.debug(f"Copy to clipboard: '{text[:50]}...'")
            except ImportError:
                logger.error("Module pyperclip non installé pour copy_to_clipboard")
                raise

        elif action == 'paste_from_clipboard':
            if not dry_run:
                pyautogui.hotkey('ctrl', 'v')
            logger.debug("Paste from clipboard")

        elif action == 'find_image':
            template_path = params['template_path']
            confidence = params.get('confidence', 0.9)
            if dry_run:
                logger.debug(f"Find image: {template_path} (confidence={confidence})")
                return {'status': 'ok', 'x': 0, 'y': 0, 'confidence': 1.0}
            try:
                import cv2
                import numpy as np
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                if template is None:
                    raise ValueError(f"Image template introuvable : {template_path}")
                screen = pyautogui.screenshot()
                screen_np = np.array(screen)
                screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val >= confidence:
                    h, w = template.shape
                    center_x = max_loc[0] + w // 2
                    center_y = max_loc[1] + h // 2
                    logger.debug(f"Image trouvée : ({center_x},{center_y}) conf={max_val:.3f}")
                    return {'status': 'ok', 'x': center_x, 'y': center_y, 'confidence': float(max_val)}
                else:
                    logger.debug(f"Image non trouvée (conf={max_val:.3f} < {confidence})")
                    return {'status': 'not_found', 'confidence': float(max_val)}
            except ImportError:
                logger.error("OpenCV non installé pour find_image")
                raise

        elif action == 'find_text_on_screen':
            text = params['text']
            lang = params.get('lang', 'fra')
            if dry_run:
                logger.debug(f"Find text: '{text}' lang={lang}")
                return {'status': 'ok', 'x': 0, 'y': 0}
            try:
                import pytesseract
                img = pyautogui.screenshot()
                data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
                n = len(data['text'])
                for i in range(n):
                    if text.lower() in data['text'][i].lower():
                        x = data['left'][i] + data['width'][i] // 2
                        y = data['top'][i] + data['height'][i] // 2
                        logger.debug(f"Texte trouvé : '{data['text'][i]}' at ({x},{y})")
                        return {'status': 'ok', 'x': x, 'y': y, 'matched_text': data['text'][i]}
                logger.debug(f"Texte non trouvé : '{text}'")
                return {'status': 'not_found'}
            except ImportError:
                logger.error("pytesseract non installé pour find_text_on_screen")
                raise

        elif action == 'wait_for_image':
            template_path = params['template_path']
            timeout = params.get('timeout', 30.0)
            interval = params.get('interval', 1.0)
            confidence = params.get('confidence', 0.9)
            start = time.time()
            while time.time() - start < timeout:
                result = execute_action('find_image', {
                    'template_path': template_path,
                    'confidence': confidence
                }, dry_run=dry_run)
                if result.get('status') == 'ok':
                    logger.info(f"Image trouvée après {time.time() - start:.2f}s")
                    return result
                time.sleep(interval)
            logger.warning(f"Timeout : image non trouvée après {timeout}s")
            return {'status': 'timeout', 'message': 'Image not found within timeout'}

        else:
            logger.warning(f"Action inconnue ou non implémentée : {action}")
            return {'status': 'error', 'message': f'Unknown action: {action}'}

        return {'status': 'ok'}

    except KeyError as e:
        logger.error(f"Paramètre manquant pour action '{action}' : {e}")
        raise
    except Exception as e:
        logger.error(f"Erreur exécution action '{action}' : {e}")
        raise

# ============ LECTURE DE MACRO ============
def play_macro(macro_path, speed=1.0, dry_run=False):
    """
    Lecture d'une macro avec gestion robuste

    Args:
        macro_path: chemin vers le fichier .json
        speed: facteur de vitesse (1.0 = normal, 2.0 = 2x plus rapide)
        dry_run: mode simulation (vérifie la validité sans exécuter)
    """
    # Validation arguments
    if speed <= 0:
        raise ValueError("Le facteur de vitesse doit être > 0")

    # Chargement
    data = load_macro(macro_path)
    events = data.get('events', [])

    logger.info(f"Lecture macro : {len(events)} événements, speed={speed}x, dry_run={dry_run}")

    if dry_run:
        logger.info("Mode dry-run : vérification seulement")
        for i, event in enumerate(events):
            try:
                execute_action(event['action'], event.get('params', {}), dry_run=True)
            except Exception as e:
                logger.error(f"Événement {i} en erreur : {e}")
                raise
        logger.info("Dry-run terminé avec succès")
        return {'status': 'ok', 'dry_run': True}

    # Exécution réelle
    start_time = time.time()
    event_index = 0
    errors = []

    while event_index < len(events):
        now = time.time() - start_time
        # Chercher le prochain événement dont le timestamp / speed <= now
        for i in range(event_index, len(events)):
            target_time = events[i]['timestamp'] / speed
            if now >= target_time:
                event = events[i]
                action = event['action']
                params = event.get('params', {})

                try:
                    execute_action(action, params, dry_run=False)
                except Exception as e:
                    logger.error(f"Erreur événement {i} (t={event['timestamp']:.3f}s, action={action}) : {e}")
                    errors.append({'index': i, 'timestamp': event['timestamp'], 'action': action, 'error': str(e)})
                event_index = i + 1
                break
        else:
            # Pas d'événement prêt, petite pause
            time.sleep(0.001)

    total_time = time.time() - start_time
    logger.info(f"Macro terminée en {total_time:.2f}s (vitesse {speed}x) — {len(errors)} erreur(s)")

    if errors:
        return {'status': 'partial', 'errors': errors, 'total_events': len(events)}
    return {'status': 'ok', 'total_events': len(events), 'duration': total_time}

# ============ POINT D'ENTRÉE ============
def main():
    if len(sys.argv) < 2:
        print("Usage: play_macro.py <macro.json> [speed]")
        sys.exit(1)

    macro_path = sys.argv[1]
    speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

    try:
        result = play_macro(macro_path, speed=speed)
        if result['status'] == 'ok':
            print("✅ Macro terminée avec succès")
            sys.exit(0)
        elif result['status'] == 'partial':
            print(f"⚠️  Macro terminée avec {len(result['errors'])} erreur(s)")
            sys.exit(1)
        else:
            print("❌ Macro terminée avec erreurs")
            sys.exit(1)
    except FileNotFoundError as e:
        logger.error(str(e))
        print(f"❌ {e}")
        sys.exit(2)
    except ValueError as e:
        logger.error(str(e))
        print(f"❌ {e}")
        sys.exit(3)
    except Exception as e:
        logger.critical(f"Erreur fatale : {e}", exc_info=True)
        print(f"❌ Erreur fatale : {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
