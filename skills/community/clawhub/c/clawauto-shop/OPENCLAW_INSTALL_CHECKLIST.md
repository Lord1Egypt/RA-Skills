# OpenClaw Install Checklist（2.0.0）

## 1. Files
- `openclaw_skill.py`
- `kfc_place_order_test_old.py` (KFC 城市+门店+预约流程)
- `kfc_custom_product_flow.py` (KFC customProduct 确认提交流程)
- `kfc_vip_choose_spec_flow.py` (KFC VIP outId 流程)
- `mcd_place_order_test.py`
- `mcd_custom_product_flow.py`
- `requirements.txt`
- `SKILL.md`

## 2. Runtime Dependencies
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## 3. Required Env Vars
```env
KFC_PLATFORM_PHONE=your_platform_phone
KFC_PLATFORM_API_KEY=your_platform_api_key
KFC_PLATFORM_BASE_URL=http://your-backend-host:8888/api/openclaw
```

Optional:
```env
KFC_PLATFORM_USERNAME=your_username
```

## 4. Backend Requirements
- Backend must expose:
  - `POST /api/openclaw/products`
  - `POST /api/openclaw/order`
- Backend must be reachable from the OpenClaw runtime machine.
- Do not rely on `localhost` unless OpenClaw and backend run on the same host.

## 5. Read-Only Validation
```bash
python openclaw_skill.py --list-products
```

Expected:
- Success: returns platform product list
- Failure:
  - `401 Unauthorized`: phone/api key mismatch
  - connection failed: backend URL not reachable

## 6. Real Order Validation
KFC flow:
```bash
python openclaw_skill.py --product-id 1 --city Shanghai --store-keyword Wanda --no-final-submit
```

McD flow:
```bash
python openclaw_skill.py --product-id 2 --store-keyword Wanda --eat-type Dine-in --no-final-submit
```

## 7. Go/No-Go
Go only if all below are true:
- `--list-products` succeeds
- Browser automation environment is available
- OpenClaw runtime can open Playwright Chromium
- Backend is reachable from OpenClaw
- Platform user has enough points
