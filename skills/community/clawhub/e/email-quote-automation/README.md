# Email Quote Automation

[中文](./README_zh.md) | English

Automated email inquiry processing and quotation generator for e-commerce and custom manufacturing businesses.

## Features

- 📥 **Automatic Email Fetching** - Connect to your mailbox via IMAP and automatically fetch unread inquiry emails
- 🌍 **Auto Translation** - Detect non-target language emails and automatically translate them
- 💾 **Structured Storage** - Organize raw emails, extracted text, translated content, and quotations in categorized folders
- 💰 **Auto Quotation Calculation** - Parse customer requirements and automatically calculate prices based on your pricing rules
- 📝 **Professional Quote Templates** - Generate ready-to-send quotation replies in both Chinese and English
- ⏰ **Scheduled Checking** - Run as a background service to periodically check for new emails

## Directory Structure

```
email-quote-automation/
├── config/                 # Configuration files
│   └── config.py           # Main configuration (you need to edit this)
├── scripts/                # Core scripts
│   ├── __init__.py
│   ├── email_check.py      # Single check for new emails
│   ├── email_daemon.py     # Scheduled background service
│   ├── email_utils.py      # Email processing utilities
│   ├── translator.py       # Translation module
│   └── quote_calculator.py # Price calculation engine
├── data/                   # Your pricing data and examples
│   ├── example/            # Example pricing data
│   │   └── pricing_rules_example.md  # Example pricing rules
│   └── README.md           # Instructions for placing your data
├── references/             # Template files
│   └── email_template.html # HTML email template
├── email_storage/          # Storage for processed emails (created automatically)
│   ├── raw/                # Original .eml files
│   ├── text/               # Extracted plain text
│   ├── translated/         # Translated content
│   └── quotes/             # Generated quotations
├── requirements.txt        # Python dependencies
├── LICENSE
├── README.md               # This file (English)
└── README_zh.md            # Chinese version
```

## Quick Start

### 1. Clone or download this project

```bash
git clone https://github.com/your-username/email-quote-automation.git
cd email-quote-automation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your settings

Edit `config/config.py`:

- **IMAP Settings**: Your email server, username and password
- **Storage Path**: Where to save processed emails
- **Translation**: Enable/disable translation and choose engine
- **Company Info**: Your information for quote replies
- **Schedule**: Check interval in minutes

### 4. Add your pricing data

Replace the example data in `data/` with your own pricing rules:

- Create your own pricing rules based on `data/example/pricing_rules_example.md`
- Update the material and process parameters in `scripts/quote_calculator.py` according to your products

See [data/README.md](./data/README.md) for detailed instructions.

### 5. Test it

Run a manual check to see if everything works:

```bash
python scripts/email_check.py
```

### 6. Run as background service (optional)

```bash
python scripts/email_daemon.py
```

## Configuration Guide

### Email Configuration (IMAP)

Common IMAP server settings:

| Email Provider | IMAP Server | Port | SSL |
|----------------|-------------|------|-----|
| QQ Mail | imap.qq.com | 993 | Yes |
| 163 NetEase | imap.163.com | 993 | Yes |
| Gmail | imap.gmail.com | 993 | Yes |
| Outlook/Hotmail | imap-mail.outlook.com | 993 | Yes |

> **Note**: Some email providers require you to enable IMAP access and use an **app password** instead of your regular password.

### Translation Engines

| Engine | Description | Requires API Key |
|--------|-------------|------------------|
| google_free | Free Google Translate (via googletrans) | No |
| baidu | Baidu Translation API | Yes |
| none | Disable automatic translation | N/A |

### Storage Structure

All processed emails are saved in the storage directory you configured (default: `./email_storage`):

- `raw/` - Original email files in `.eml` format (can be opened in any email client)
- `text/` - Extracted plain text content with metadata
- `translated/` - Translated content (only created if translation is enabled)
- `quotes/` - Generated quotation text files ready for sending

## Example: How It Works

1. Customer sends an inquiry email:
   > "Hi, I need 10 custom crystal medals, 20cm diameter with UV printing and wooden boxes."

2. The tool automatically:
   - Fetches the email from your inbox
   - Detects it's in English and translates to Chinese
   - Parses the requirements: 10 × Crystal 20cm + UV printing + wooden box
   - Calculates price: `(120 × 1.0 + 10 + 35) × 10 × 0.95 = ¥1567.50`
   - Generates a professional quotation reply in both English and Chinese
   - Saves everything to the organized directories
   - Marks the email as read

3. You just review the generated quote and send it to your customer!

## Customization

### Changing Pricing Rules

Edit `scripts/quote_calculator.py` and modify these variables:

- `MATERIAL_PRICES` - Your material base prices
- `SIZE_COEFFICIENTS` - Size-based price coefficients
- `PROCESS_FEES` - Additional process fees
- `DISCOUNTS` - Quantity-based discount tiers

### Adding More Translation Engines

Add your engine in `scripts/translator.py` - see the existing Google and Baidu implementations as reference.

### Using Different Templates

Edit `references/email_template.html` for custom HTML email templates.

## Use Cases

This tool is perfect for:

- 🏆 **Medal/Trophy custom manufacturing** - (original use case)
- 👕 **Custom apparel and merchandise**
- 🖨️ **Printing and packaging services**
- 🪑 **Custom furniture and woodworking**
- 📦 **Light manufacturing and wholesale**
- Any business that receives price inquiries via email and has standard pricing rules

## Requirements

- Python 3.7+
- `pandas` - for data handling
- `langdetect` - for language detection
- `googletrans` - for free Google translation (optional)
- IMAP-enabled email account

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Contributing

Issues and pull requests are welcome!

## Screenshots

*(Add your screenshots here after setup)*

