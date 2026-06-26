# Everything CLI Search - Installation Guide

## ✅ Skill đã được cài đặt thành công!

Skill Everything CLI Search đã được copy về các vị trí sau:
- `C:\Users\Anna\.openclaw\skills\everything-cli-search\`
- `C:\Users\Anna\.openclaw\.agent\skills\everything-cli-search\`
- `C:\Users\Anna\.openclaw\workspace\skills\everything-cli-search\`

## ⚠️ Cần cài đặt Everything

Để sử dụng skill này, bạn cần cài đặt Everything trước:

### Bước 1: Tải và cài đặt Everything

1. Truy cập https://www.voidtools.com
2. Tải Everything (phiên bản mới nhất)
3. Chạy file cài đặt và làm theo hướng dẫn

### Bước 2: Enable Everything Service

1. Mở Everything
2. Đi đến **Tools** → **Options** → **General**
3. Check **"Run as service"**
4. Click **OK**
5. Restart Everything

### Bước 3: Tải es.exe (Bắt buộc)

**Quan trọng**: `everything.exe` là GUI application và không hỗ trợ command line interface. Bạn cần tải `es.exe` (Everything Command Line Interface) riêng biệt.

1. Truy cập https://www.voidtools.com/downloads/
2. Tìm phần "Command Line Interface" hoặc "ES"
3. Tải file es.exe.zip
4. Giải nén và copy es.exe vào:
   - `E:\Computer\Everything\` (khuyên dùng)
   - Hoặc thêm vào System PATH

### Bước 4: Thêm es.exe vào PATH (tùy chọn)

Nếu bạn muốn sử dụng `es.exe` từ bất kỳ đâu:

1. Nhấn Win + X, chọn **System**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Trong **System variables**, tìm **Path** và click **Edit**
5. Click **New** và thêm đường dẫn: `E:\Computer\Everything`
6. Click **OK** để đóng tất cả cửa sổ

### Bước 5: Kiểm tra cài đặt

Mở Command Prompt hoặc PowerShell và chạy:

```bash
es.exe "test"
```

Nếu bạn thấy kết quả tìm kiếm, Everything CLI đã sẵn sàng sử dụng!

## 📚 Tài liệu

- **README.md** - Hướng dẫn nhanh
- **SKILL.md** - Tài liệu chi tiết đầy đủ
- **EXAMPLES.md** - Ví dụ thực tế

## 🚀 Bắt đầu sử dụng

### Tìm kiếm cơ bản

```bash
# Tìm file
es.exe "filename.txt"

# Tìm với wildcard
es.exe "*.pdf"

# Tìm trong thư mục cụ thể
es.exe -p "C:\Users\Documents" "report"
```

### Tìm kiếm nâng cao

```bash
# Tìm file lớn hơn 1MB được sửa hôm nay
es.exe "*.pdf size:>1mb datemodified:today"

# Tìm file audio
es.exe "audio:"

# Tìm file ẩn
es.exe "attrib:H"
```

## 📝 Scripts

Skill bao gồm 3 scripts:

### Python Script

```bash
python3 everything_search.py "query"
```

### Bash Script

```bash
./es_search.sh "query"
```

### PowerShell Script

```bash
.\es_search.ps1 "query"
```

## 🔗 Liên kết hữu ích

- [Everything Documentation](https://www.voidtools.com/support/everything/)
- [Everything Download](https://www.voidtools.com/)
- [Command Line Options](https://www.voidtools.com/support/everything/command_line_options)

## ❓ Trợ giúp

Nếu bạn gặp vấn đề:

### "es.exe not found"

1. Kiểm tra Everything đã được cài đặt
2. Thêm đường dẫn Everything vào PATH
3. Restart terminal

### Không có kết quả

1. Đảm bảo Everything service đang chạy
2. Kiểm tra đường dẫn tìm kiếm
3. Thử rebuild database: `es.exe -reindex`

### Tìm kiếm chậm

1. Đảm bảo Everything service đã được enable
2. Kiểm tra NTFS indexing
3. Enable fast sorting options

## ✨ Tính năng chính

- **Tìm kiếm nhanh**: Kết quả tức thì với bộ lọc nâng cao
- **Command Line Interface**: Hỗ trợ đầy đủ es.exe
- **Multiple Scripts**: Python, Bash, PowerShell
- **Advanced Syntax**: Operators, wildcards, macros, modifiers
- **Remote Access**: HTTP và ETP server
- **File Lists**: Index offline media (CDs, DVDs, etc.)
- **Keyboard Shortcuts**: Phím tắt đầy đủ

## 🎯 Sẵn sàng!

Sau khi cài đặt Everything, bạn có thể sử dụng skill này để tìm kiếm file cực nhanh trên Windows!

---

**Created**: 2026-03-28
**Skill Version**: 1.0
**Everything Version**: Latest
