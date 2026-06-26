import json, pathlib, os

CONFIG = pathlib.Path('/root/.openclaw/openclaw.json')
SECRET_DIR = pathlib.Path('/root/.openclaw/secrets')
MODELS_FILE = pathlib.Path('/root/.openclaw/scripts/model_manager/available_models.json')

def update_9router_config(api_key, model_id, model_name):
    # Đọc config hiện tại
    data = json.loads(CONFIG.read_text())
    # Cập nhật provider 9router
    if 'models' not in data: data['models'] = {'providers': {}}
    if 'providers' not in data['models']: data['models']['providers'] = {}
    
    data['models']['providers']['openrouter_auto'] = {
        "api": "openai-completions",
        "apiKey": api_key,
        "baseUrl": "https://openrouter.ai/api/v1",
        "models": [{"id": model_id, "name": model_name}]
    }
    CONFIG.write_text(json.dumps(data, indent=2))
    os.system('openclaw gateway restart')
    print(f"Added {model_name} to 9Router.")

if __name__ == "__main__":
    # Load key từ file bí mật (anh tạo file này)
    token_file = SECRET_DIR / 'openrouter.token'
    if token_file.exists():
        key = token_file.read_text().strip()
        # Giả sử đã quét và chọn model từ available_models.json / assume we already scanned and selected a model from available_models.json
        update_9router_config(key, "google/gemini-2.0-flash-lite:free", "Gemini 2.0 Flash Lite")
