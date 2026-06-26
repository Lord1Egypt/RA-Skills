# Facebook Post Reader (skill mẫu)

Mô tả:
- Skill này cố gắng truy cập một URL (ví dụ profile hoặc bài viết) và lấy nội dung "bài viết đầu tiên" trên trang đó.
- Lưu ý: Facebook và nhiều trang hiện đại sử dụng JavaScript/đăng nhập; script này là "server-side scraping" đơn giản và có thể không hoạt động với các trang yêu cầu JS hoặc đăng nhập. Xem phần "Lưu ý" bên dưới.

Input:
- url (string): URL trang web cần đọc

Output (JSON):
- status: "success" hoặc "error"
- content: nội dung văn bản đã lấy hoặc thông báo lỗi

Cấu trúc file:
- SKILL.md
- manifest.json
- scripts/skill.py
- requirements.txt
- references/schema.md
- references/queries.md

Lưu ý quan trọng:
- Nếu trang yêu cầu đăng nhập (như Facebook cá nhân), script này có thể không lấy được nội dung.
- Để xử lý Facebook / trang động, cần dùng browser automation (Puppeteer/Playwright) với cookie đã đăng nhập.
- Dùng skill này đúng pháp luật và chính sách của nền tảng khi crawl nội dung.
