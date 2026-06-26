from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import datetime
import json

# Add parent directory to path to import suno_client
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.suno_client import AceSunoClient

app = Flask(__name__)

# Configuration
BASE_MUSIC_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "music")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'generation_history.json')

# Create directories if they don't exist
os.makedirs(BASE_MUSIC_DIR, exist_ok=True)
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)


def save_to_history(track_info):
    """Save generated track to history"""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    
    history.insert(0, track_info)
    # Keep only last 50 entries
    if len(history) > 50:
        history = history[:50]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def get_history():
    """Get generation history"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Handle music generation request"""
    try:
        data = request.get_json()
        api_key = data.pop('api_key', None)
        
        client = AceSunoClient(api_key=api_key)
        
        # Extract parameters from request - only add when true or non-empty
        params = {
            'action': data.get('action', 'generate'),
            'prompt': data.get('prompt', ''),
            'model': data.get('model', 'chirp-v5'),
        }
        
        # Only add boolean params when true
        custom_val = data.get('custom', False)
        if custom_val:
            params['custom'] = True
        
        instrumental_val = data.get('instrumental', False)
        if instrumental_val:
            params['instrumental'] = True
        
        # Add optional parameters if provided
        optional_fields = [
            'lyric', 'title', 'style', 'style_negative', 'audio_weight', 
            'audio_id', 'vocal_gender', 'weirdness', 'lyric_prompt', 'callback_url',
            'overpainting_start', 'overpainting_end', 'underpainting_start', 'underpainting_end',
            'persona_id', 'continue_at', 'style_influence', 'replace_section_end', 'replace_section_start'
        ]
        for field in optional_fields:
            if field in data and data[field] not in ['', None]:
                if field in ['audio_weight', 'overpainting_start', 'overpainting_end', 
                           'underpainting_start', 'underpainting_end', 'continue_at', 
                           'style_influence', 'replace_section_end', 'replace_section_start']:
                    params[field] = float(data[field])
                elif field == 'weirdness':
                    params[field] = int(data[field])
                else:
                    params[field] = data[field]
        
        # Call API
        try:
            response = client.generate(**params)
        except Exception as e:
            # Return parameters for debugging
            error_msg = f"{str(e)}\n\nSent parameters:\n{repr(params)}"
            return jsonify({'error': error_msg, 'params': params}), 400
        
        if not response.get('success'):
            error_msg = response.get('message', 'Generation failed')
            return jsonify({'error': error_msg, 'params': params, 'response': response}), 400
        
        # Save files to desktop
        output_dir = client.save_generation(response['data'], BASE_MUSIC_DIR)
        
        # Save to history
        for track in response['data']:
            track_info = {
                'id': track['id'],
                'title': track.get('title', 'Untitled'),
                'prompt': params.get('prompt', ''),
                'model': params.get('model'),
                'created_at': track.get('created_at'),
                'duration': track.get('duration'),
                'audio_url': track.get('audio_url'),
                'image_url': track.get('image_url'),
                'local_dir': output_dir,
                'file_name': f"{track.get('title', 'untitled').replace(' ', '_')}_{track['id']}.mp3"
            }
            save_to_history(track_info)
        
        return jsonify({
            'success': True,
            'output_dir': output_dir,
            'tracks': response['data']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/history')
def history():
    """Get generation history"""
    return jsonify(get_history())


@app.route('/download/<date>/<filename>')
def download(date, filename):
    """Download generated file"""
    directory = os.path.join(BASE_MUSIC_DIR, date)
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/music/<path:filename>')
def serve_music(filename):
    """Serve music file for playback"""
    return send_from_directory(BASE_MUSIC_DIR, filename)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the server"""
    import os
    os._exit(0)


if __name__ == '__main__':
    app.run(debug=True, port=1688)
