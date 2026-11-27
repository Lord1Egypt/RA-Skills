# HƯỚNG DẪN IMPORT SKILL `meta-ads-report` SANG MÁY KHÁC

Skill này chỉ gồm 1 file `SKILL.md`. Không cần cài package gì thêm (chỉ dùng `curl`).

---

## Bước 1 — Copy file sang máy đích

Đặt file vào **workspace của agent** trên máy đó, trong thư mục `skills/`:

```
<workspace-agent>/skills/meta-ads-report/SKILL.md
```

Ví dụ (Linux, OpenClaw mặc định):

```bash
mkdir -p ~/.openclaw/workspace-<agent>/skills/meta-ads-report
# chép SKILL.md vào đó (scp / USB / copy-paste tay đều được)
```

> OpenClaw tự quét `workspace/skills/*/SKILL.md`. Sau khi copy → mở session mới (hoặc restart gateway) là skill xuất hiện trong `<available_skills>`.

---

## Bước 2 — Đặt biến môi trường trên máy đích

Skill cần **2 biến**, KHÔNG hardcode vào file. Thêm vào mục `env` trong config gateway (`openclaw.json`):

```json
"env": {
  "META_ACCESS_TOKEN": "<token-của-agent-đó>",
  "META_AD_ACCOUNT_ID": "<id-tkqc-mặc-định>"
}
```

Rồi restart gateway.

- Token của **mỗi máy phải tự lấy riêng** (`developers.facebook.com/tools/explorer`, quyền `ads_read`).
- `META_AD_ACCOUNT_ID` để **số trần**, KHÔNG có prefix `act_` (ví dụ `123456789`).
- ⚠️ Token cá nhân long-lived sống ~60 ngày → hết hạn phải login lại lấy token mới.

---

## Bước 3 — Kiểm tra chạy được

```bash
curl -s -G "https://graph.facebook.com/v21.0/debug_token" \
  --data-urlencode "input_token=$META_ACCESS_TOKEN" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

Thấy `"is_valid": true` là OK. Rồi thử kéo 1 báo cáo 7 ngày xem ra số.

---

## ⚠️ 3 cái bẫy hay gặp (đọc kỹ)

1. **"Token hết hạn" GIẢ** — Do nhét token thẳng vào URL bằng ngoặc kép → shell cắt chuỗi → lỗi 4xx.
   → Luôn dùng: `curl -G --data-urlencode "access_token=$META_ACCESS_TOKEN" ...`

2. **Thiếu `access_token` trong URL** → lỗi `(#200) Provide valid app ID` dù token còn hạn.
   → Nhớ truyền `access_token` ở MỌI request.

3. **Thiếu prefix `act_`** khi gọi bằng ad account ID → sai endpoint.
   → `act_123456789`, không phải `123456789`.

---

## Tùy chọn — Publish lên ClawHub (nếu muốn chia sẻ rộng / nhiều máy)

Nếu máy đích cũng chạy OpenClaw và muốn cài tự động:

```bash
# trên máy đích, dùng skill clawhub
openclaw skills install <tên-skill-trên-clawhub>
```

Hoặc đóng gói thư mục skill rồi publish lên ClawHub để các máy khác `install` 1 lệnh. Xem skill `clawhub` để biết cú pháp publish/install chính xác theo phiên bản.
