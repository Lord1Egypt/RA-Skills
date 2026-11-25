# CÀI ĐẶT — Hướng dẫn cho người dùng cuối

Tài liệu này dành cho **người dùng bình thường**, không cần biết code.
Bạn chỉ cần một agent OpenClaw đang chạy (Telegram, Zalo, Discord… đều được).

**Skill này làm gì:** cho agent quyền tự tạo và sửa Google Sheet / Google Drive
trong tài khoản Google của **chính bạn** — tạo folder, tạo Sheet, ghi số liệu,
định dạng, sắp xếp. Không cần service account, không cần vào Google Cloud Console
bằng tay (agent làm hết).

---

## Bước 1 — Tải file zip

Tải file `google-sheets-connect-1.2.1.zip` (người gửi đưa kèm trong chat).

## Bước 2 — Mở chat với agent của bạn và gửi file

- Trên **Telegram**: bấm biểu tượng 📎 → chọn file vừa tải → gửi vào chat với agent.
- Trên kênh khác (Zalo / Discord / Web): dùng nút đính kèm tương tự.

## Bước 3 — Copy câu lệnh dưới đây, dán vào chat và gửi

```
Tôi vừa gửi 1 file zip skill google-sheets-connect. Hãy giải nén và cài skill này
vào workspace của bạn, rồi hướng dẫn tôi hoàn tất bước cấp quyền Google.
```

Agent sẽ tự làm: giải nén → cài vào `skills/` → kiểm tra chạy được. Bạn không phải
gõ lệnh gì. Nếu agent hỏi lại đường dẫn file, cứ trả lời "file zip tôi vừa gửi".

## Bước 4 — Tạo app OAuth Google (agent sẽ hướng dẫn, ~5 phút, làm 1 lần)

Đây là phần **bắt buộc** — Google yêu cầu mỗi người tự tạo "chìa khoá" riêng cho
agent của mình. Agent sẽ dẫn bạn từng bước, tóm tắt là:

1. Vào `console.cloud.google.com` → tạo project mới (tên gì cũng được).
2. **APIs & Services → Library** → bật **Google Drive API** và **Google Sheets API**.
3. **OAuth consent screen** → chọn **External** → điền tên app + email của bạn
   → thêm email của bạn vào ô **Test users**.
4. **Credentials → Create credentials → OAuth client ID → Desktop app**
   → copy về 2 mã: **Client ID** và **Client secret**.
5. Gửi 2 mã đó cho agent, kèm câu: *"Đây là Client ID và Client secret của tôi,
   hãy lưu lại."* Agent sẽ lưu vào máy với quyền hạn chế, không in ra chat.

> 💡 Muốn phiên đăng nhập không hết hạn sau 7 ngày → sau khi tạo app, vào
> **OAuth consent screen** bấm **Publish app**.

## Bước 5 — Bấm Allow và dán mã

Agent sẽ gửi bạn 1 **đường link Google**. Bạn làm:

1. Bấm link → chọn đúng tài khoản Google → **Allow**.
2. Google hiện ra một **mã code** (dạng `4/0A...`) → copy.
3. Dán mã đó vào chat và gửi cho agent.

Agent sẽ báo lại: đã kết nối email nào, quota Drive bao nhiêu, và chạy bài test
thật (tạo folder → tạo Sheet → ghi → định dạng → đọc → xoá).

**Khi thấy agent báo "Đã kết nối Drive của <email>" là xong.**

---

## Sau khi cài xong, bạn dùng được gì

Chỉ cần nói bằng tiếng Việt bình thường:

- *"Tạo cho tôi một Google Sheet tên BÁO CÁO TUẦN trong folder Drive, ghi bảng số liệu này vào."*
- *"Mở Sheet này, thêm tab Tổng quan và định dạng tiêu đề đậm nền vàng."*
- *"Đọc dữ liệu tab Khách hàng từ dòng 2 đến dòng 50."*
- *"Liệt kê các file tôi có trong folder BÁO CÁO T10."*

## Cần biết trước (để không bất ngờ)

| Điều | Giải thích |
|---|---|
| Vẫn phải bấm Allow 1 lần | Google bắt buộc, không có cách nào bỏ qua |
| Mỗi người tự tạo app OAuth riêng | Không dùng chung "chìa khoá" của người khác |
| Chỉ sửa được file đã share cho tài khoản đã kết nối | File riêng của người khác thì chưa đụng được |
| Phiên có thể hết hạn sau 7 ngày | Nếu app còn ở chế độ Testing → bấm Publish app |
| Agent xoá file/tab luôn hỏi lại trước | Đây là thiết kế an toàn, không phải lỗi |
| Mất mật khẩu / đổi mật khẩu Google | Phải kết nối lại từ Bước 5 |

## Cập nhật skill sau này

Bản cài bằng file zip **không tự cập nhật**. Khi có bản mới, người gửi sẽ đưa zip
mới — bạn gửi lại vào chat và nói:

```
Cập nhật skill google-sheets-connect lên bản mới trong file zip tôi vừa gửi,
giữ nguyên phiên đăng nhập Google hiện tại.
```

## Gặp lỗi thì nói gì với agent

Cứ copy nguyên câu lỗi agent hiện ra và gửi lại, kèm: *"Lỗi này xử lý thế nào?"*
Đừng tự sửa gì — agent đọc được lỗi và biết cách xử lý.
