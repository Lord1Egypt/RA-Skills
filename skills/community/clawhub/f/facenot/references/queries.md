# Tham chiếu truy vấn / ví dụ

Ví dụ gọi script từ command-line:

```
python3 scripts/skill.py --url "https://www.facebook.com/profile.php?id=100089883616175"
```

Kết quả: JSON in ra stdout, ví dụ:

{
  "status": "success",
  "content": "Nội dung bài viết đầu tiên..."
}

Nếu trang không trả HTML tĩnh (ví dụ Facebook cần JS/login), script sẽ trả lỗi với content mô tả nguyên nhân.
