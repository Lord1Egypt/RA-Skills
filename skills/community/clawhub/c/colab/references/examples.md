# Colab Examples

## CIFAR-10 Training (T4 GPU)

```bash
python3 tools/colab/colab_run.py exec --gpu T4 --file experiments/cifar10/cifar10_colab.py
```

Result: 88.28% test accuracy, 4m11s on T4. SmallResNet (2.6M params), 10 epochs, cosine schedule.

## F5-TTS Voice Clone

Template at `experiments/tts/colab_tts_clean.py`. Inject reference audio as base64:

```python
# Template variables to replace:
REF_AUDIO_B64 = "__REF_AUDIO__"     # base64-encoded wav
TEXT = "__GEN_TEXT__"                 # text to speak
```

Result: 12.5s audio in 29s generation time (RTF 2.34x) on T4.

## Drive Round-Trip

Template at `experiments/test_drive_roundtrip.py`. Uses `__COLAB_TOKEN_PLACEHOLDER__` for token injection.

```bash
bash tools/colab/inject_and_run.sh experiments/test_drive_roundtrip.py
```

## Long Training with Checkpoints

```python
"""Template: training with Drive checkpointing."""
import json, base64, os, sys, torch

# --- Drive setup (token injected by inject_and_run.sh) ---
TOKEN_B64 = "__COLAB_TOKEN_PLACEHOLDER__"
token_data = json.loads(base64.b64decode(TOKEN_B64))
with open('/tmp/token.json', 'w') as f:
    json.dump(token_data, f)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

creds = Credentials.from_authorized_user_file('/tmp/token.json')
service = build('drive', 'v3', credentials=creds)

# Find workspace folder
folder_r = service.files().list(
    q="name='colab-workspace' and mimeType='application/vnd.google-apps.folder' and trashed=false",
    fields='files(id)'
).execute()
FOLDER_ID = folder_r['files'][0]['id']

def save_checkpoint(model, optimizer, epoch, path='/tmp/checkpoint.pt'):
    torch.save({'epoch': epoch, 'model': model.state_dict(), 'optimizer': optimizer.state_dict()}, path)
    media = MediaFileUpload(path, mimetype='application/octet-stream')
    # Delete old checkpoint if exists
    old = service.files().list(q=f"name='checkpoint.pt' and '{FOLDER_ID}' in parents", fields='files(id)').execute()
    for f in old.get('files', []):
        service.files().delete(fileId=f['id']).execute()
    service.files().create(body={'name': 'checkpoint.pt', 'parents': [FOLDER_ID]}, media_body=media).execute()
    print(f'Checkpoint saved: epoch {epoch}')

def load_checkpoint(model, optimizer):
    results = service.files().list(q=f"name='checkpoint.pt' and '{FOLDER_ID}' in parents", fields='files(id)').execute()
    if not results.get('files'):
        return 0
    fh = io.BytesIO()
    request = service.files().get_media(fileId=results['files'][0]['id'])
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    ckpt = torch.load(fh, weights_only=False)
    model.load_state_dict(ckpt['model'])
    optimizer.load_state_dict(ckpt['optimizer'])
    return ckpt['epoch']

# --- Training loop ---
# model = ...
# optimizer = ...
# start_epoch = load_checkpoint(model, optimizer)
# for epoch in range(start_epoch, total_epochs):
#     train(...)
#     if epoch % checkpoint_every == 0:
#         save_checkpoint(model, optimizer, epoch)
```
