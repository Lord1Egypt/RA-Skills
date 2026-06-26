"""
Simple web interface for Error Log Analyzer
"""
from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import LogAnalyzer

app = Flask(__name__)
analyzer = LogAnalyzer()


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze log content."""
    try:
        data = request.get_json()
        log_content = data.get('logs', '')
        
        if not log_content:
            return jsonify({'error': 'No log content provided'}), 400
        
        results = analyzer.analyze(log_content)
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/upload', methods=['POST'])
def upload():
    """Upload and analyze log file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        content = file.read().decode('utf-8')
        
        # Analyze
        results = analyzer.analyze(content)
        
        return jsonify({
            'success': True,
            'results': results,
            'filename': file.filename
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
