# AutoPost GitHub Bounty Campaign

## Mô tả
Kỹ năng này tự động tạo nội dung chia sẻ cho các chiến dịch Bounty trên GitHub. Giúp đăng bài hiệu quả để tăng lượt tham gia và hoàn thành yêu cầu của bounty.

---

### Tính năng
1. Lấy tiêu đề và mô tả từ repository GitHub.
2. Tạo bài viết với nội dung tối ưu hóa kêu gọi hành động (CTA).
3. Gửi bài qua mạng xã hội (Twitter, Facebook, etc.).

---

### Cấu hình yêu cầu
- API Token GitHub (để lấy thông tin repo).
- API Token các nền tảng xã hội (Twitter, etc.).

---

## Hướng dẫn cài đặt
1. Clone repo:
```bash
git clone https://github.com/<user>/clawhub-skill-autopost.git
```
2. Cài đặt dependencies:
```bash
npm install
```
3. Chạy skill:
```bash
node autopost.js --repo <repo_url> --platform "twitter" --message "<custom_message>"
```