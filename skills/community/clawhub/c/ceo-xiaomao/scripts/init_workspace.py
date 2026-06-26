#!/usr/bin/env python3
"""
CEO小茂 workspace initializer
Usage: python3 scripts/init_workspace.py
"""
import os, json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR   = os.environ.get('XIAONENG_DIR', os.path.dirname(SCRIPT_DIR))

TEMPLATES = {
    '.known_customers.json': json.dumps([], ensure_ascii=False, indent=2),
    '.product_db.json': json.dumps({
        "product_name": "[Product Name]",
        "product_info": "Product: [Product Name]\nFeatures: [Feature Summary]\nWarranty: [Warranty]\nMOQ: [MOQ]\nTerms: FOB / CIF / EXW available\n",
        "catalog": [],
        "images": [],
        "videos": [],
        "fallback_image_url": ""
    }, ensure_ascii=False, indent=2),
    '.boss_notifications.json': json.dumps([], ensure_ascii=False, indent=2),
    '.auto_state_v3.json': json.dumps({"baseline": {}, "replied_at": {}, "lang_profile": {}}, ensure_ascii=False, indent=2),
    'body.txt': "Hello, we are a professional manufacturer from China. We would be glad to share our catalog and business details.",
    'customers.example.csv': 'phone,message\n8610000000000,Hello from your business team.\n',
    'leads.example.csv': 'company,email,phone,address,website,notes\nExample Corp,contact@example.com,+1 000 000 0000,123 Main St,https://example.com,Priority\n',
    'send_log.csv': 'time,email,status,note\n',
    'README-SETUP.md': """# CEO小茂 setup

## Generated files
- `.known_customers.json`
- `.product_db.json`
- `.boss_notifications.json`
- `.auto_state_v3.json`
- `body.txt`
- `customers.example.csv`
- `leads.example.csv`
- `send_log.csv`

## Suggested environment variables

```bash
export GREEN_API_URL=\"https://your-service.example\"
export GREEN_API_INSTANCE_ID=\"your_instance\"
export GREEN_API_CREDENTIAL=\"your_credential\"
export MAIL_ACCOUNT=\"your@mail.com\"
export MAIL_CREDENTIAL=\"your_mail_credential\"
export ONEABC_ACCESS_CREDENTIAL=\"your_credential\"
export XIAONENG_DIR=\"$(pwd)\"
```
""",
}

def main():
    print("🎯 CEO小茂 workspace initializer")
    print(f"Workspace: {WORK_DIR}\n")
    os.makedirs(WORK_DIR, exist_ok=True)
    for fname, content in TEMPLATES.items():
        path = os.path.join(WORK_DIR, fname)
        if os.path.exists(path):
            print(f"skip: {fname}")
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"created: {fname}")
    print("\nDone.")

if __name__ == '__main__':
    main()
