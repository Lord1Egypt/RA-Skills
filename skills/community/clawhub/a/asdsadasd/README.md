# 🤖 OpenClaw AI Agentic Facebook Auto-Post

> **Stack:** OpenClaw (ClawHub) · Apify · GPT-4o · DALL-E 3 · Facebook Graph API v21.0  
> **Target:** Production-ready | Automated content pipeline

---

## Kiến trúc pipeline

```
URL (báo / FB post)
    ↓
[Agent 1] Crawler (Apify)        → raw content
    ↓
[Agent 2] Writer (GPT-4o)        → post text + hashtags + image prompt
    ↓
[Agent 3] Image Gen (DALL-E 3)   → ảnh thumbnail
    ↓
[Agent 4] FB Publisher (Graph API) → đăng lên Fanpage
```

---

## Setup nhanh (5 bước)

### Bước 1: Cài thư viện
```bash
pip install -r requirements.txt
```

### Bước 2: Điền .env
Mở file `.env` — đã có sẵn App ID, API keys. Chỉ cần điền:
```env
FB_USER_ACCESS_TOKEN=   ← lấy từ bước 3
FB_PAGE_ACCESS_TOKEN=   ← lấy từ bước 3
```

### Bước 3: Lấy Facebook Page Token
```bash
python agents/fb_token_helper.py
```
Làm theo hướng dẫn → copy Page Access Token vào `.env`.

### Bước 4: Test kết nối
```bash
python test_fb_connection.py
```
Phải thấy 3 dấu ✅ xanh.

### Bước 5: Chạy pipeline!
```bash
# Crawl từ link báo → viết bài → tạo ảnh → đăng FB
python main.py --url "https://dantri.com.vn/..."

# Crawl từ bài post FB public
python main.py --url "https://www.facebook.com/..."

# Test đăng bài a (không crawl)
python main.py --test-post

# Dry run (không đăng thật, xem kết quả trong output/)
python main.py --url "https://..." --dry-run

# Không tạo ảnh (nhanh hơn, tiết kiệm credit)
python main.py --url "https://..." --no-image

# Lên lịch đăng
python main.py --url "https://..." --schedule 1735689600
```

---

## Cấu trúc thư mục

```
OpenClaw_Analyze/
├── agents/
│   ├── crawler_agent.py        # Crawl news/FB post via Apify
│   ├── writer_agent.py         # GPT-4o viết bài FB + hashtag + image prompt
│   ├── image_agent.py          # DALL-E 3 tạo ảnh thumbnail
│   ├── fb_publisher_agent.py   # Đăng lên Facebook Fanpage
│   └── fb_token_helper.py      # Tool lấy/exchange FB token
├── skills/
│   └── facebook/
│       └── SKILL.md            # OpenClaw skill reference
├── output/                     # Kết quả run (tạo tự động)
│   └── images/                 # Ảnh DALL-E đã download
├── config.py                   # Centralized config từ .env
├── main.py                     # Orchestrator CLI
├── test_fb_connection.py       # Kiểm tra kết nối FB
├── .env                        # 🔒 Secrets (không commit!)
├── .env.example                # Template cho team
└── requirements.txt
```

---

## Credentials đã có

| Service | Key |
|---------|-----|
| OpenAI | `sk-proj-Z-KB75Z...` |
| Apify | `apify_api_BdeZ...` |
| FB App ID | `4348763312075291` |
| FB Page ID | `61565210956273` |

> **Còn thiếu:** `FB_PAGE_ACCESS_TOKEN` — chạy `fb_token_helper.py` để lấy.

---

## Lưu ý quan trọng

- `.env` đã có trong `.gitignore` — **không bao giờ commit file này**
- DALL-E URL chỉ hợp lệ ~1 giờ — pipeline tự dùng ngay để upload FB
- Rate limit FB: tối đa ~200 API calls/giờ; code đã có retry backoff
- Post tối đa 4-5 bài/ngày để tránh bị flag spam

---

## Troubleshooting

| Lỗi | Fix |
|-----|-----|
| `FB_PAGE_ACCESS_TOKEN chưa set` | Chạy `python agents/fb_token_helper.py` |
| `Error 190: Token expired` | Chạy lại `fb_token_helper.py` để refresh |
| `Apify actor timeout` | URL quá phức tạp → thử URL bài đơn giản hơn |
| `openai.RateLimitError` | Kiểm tra billing OpenAI account |
| `No items crawled` | URL có thể bị chặn bot → thử URL khác |
