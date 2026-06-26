# Setup Guide — Cutout.Pro Visual API Skill

## 1. Create an Account

1. Visit **https://www.cutout.pro**
2. Click **Sign Up** to register (or log in if you already have an account)
3. Supports Google, GitHub, or email registration

## 2. Get Your API Key

1. After logging in, go to: https://www.cutout.pro/user/secret-key
2. Click **Create API Key** to generate a key
3. Copy the generated key (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

## 3. Configure the Key

Create a `.env` file in the skill root directory:

```
CUTOUT_API_KEY=your_api_key_here
```

Or export it as an environment variable:

```bash
export CUTOUT_API_KEY="your_api_key_here"
```

## 4. Install Dependencies

```bash
cd cutout-visual-api
pip install -r scripts/requirements.txt
```

The only external dependency is **requests** (HTTP client library).

## 5. Test the Connection

```bash
python scripts/cutout.py --api bg-remover --image /path/to/test.jpg --preview
```

If the key is configured correctly, the processed image will be saved to `data/outputs/`.

## 6. First Call

```bash
# Background removal
python scripts/cutout.py --api bg-remover --image photo.jpg --output result.png

# Face cutout
python scripts/cutout.py --api face-cutout --image portrait.jpg --output face.png

# Photo enhancement
python scripts/cutout.py --api photo-enhancer --image blurry.jpg --output hd.png
```

## Troubleshooting

### Error 1001 (Insufficient Balance)
- Check your credit balance at: https://www.cutout.pro/user/account
- Top up credits or use preview mode (`--preview`, costs 0.25 credits)

### Error 401 (Unauthorized)
- Verify the key in your `.env` file is correct
- Make sure there are no extra spaces in the key
- Generate a new key from the dashboard

### Error 400 (Bad Request)
- Check that the image file exists and the format is supported (PNG/JPG/JPEG/BMP/WEBP)
- Check that the image resolution does not exceed 4096×4096
- Check that the file size does not exceed 15 MB

### Image Not Saved
- Check write permissions for the `data/outputs/` directory
- The directory is created automatically, but may fail in restricted environments

## Quota Details

| Mode | Credit Cost | Max Resolution |
|------|-------------|----------------|
| Standard | 1 credit/image | 4096×4096 |
| Preview (`--preview`) | 0.25 credits/image | 500×500 |

## Security Notes

- The API Key will never appear in logs or output
- The `.env` file is in `.gitignore` — do not commit it to version control
- The daily processing limit can be configured via the `CUTOUT_MAX_IMAGES_PER_DAY` environment variable (default: 100)
