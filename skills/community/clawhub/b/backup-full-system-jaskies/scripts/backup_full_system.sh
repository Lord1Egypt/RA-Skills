#!/bin/bash

# 1. ĐỊNH NGHĨA
PARENT_DIR="/home/jackie_chen_phong"
SOURCE_NAME=".openclaw"
BACKUP_DIR="$PARENT_DIR/backups"
TMP_DIR="$PARENT_DIR/full_system_info"
DATE=$(date +%Y-%m-%d_%Hh%M)
FILENAME="Ultimate_Snapshot_$DATE.tar.gz"

mkdir -p $BACKUP_DIR $TMP_DIR

echo "--- ĐANG QUÉT TOÀN BỘ CẤU HÌNH HỆ THỐNG ---"

# 2. SAO LƯU DANH SÁCH PHẦN MỀM & CRON
apt-mark showmanual > $TMP_DIR/apt_packages.txt
pip list --format=freeze > $TMP_DIR/python_libraries.txt 2>/dev/null
crontab -l > $TMP_DIR/crontab_bak.txt 2>/dev/null

# 3. SAO LƯU FILE CẤU HÌNH NGƯỜI DÙNG (Biến môi trường)
cp ~/.bashrc ~/.profile ~/.bash_logout $TMP_DIR/ 2>/dev/null
cp -r ~/.config $TMP_DIR/user_configs 2>/dev/null

# 4. SAO LƯU CẤU HÌNH HỆ THỐNG (Cần quyền sudo cho các file nhạy cảm)
# Sao lưu cấu hình Tailscale (nếu có)
if [ -d "/etc/tailscale" ]; then
    sudo cp -r /etc/tailscale $TMP_DIR/etc_tailscale 2>/dev/null
fi
# Sao lưu các file dịch vụ tự tạo (Systemd)
sudo cp /etc/systemd/system/openclaw* $TMP_DIR/systemd_services 2>/dev/null

# 5. SAO LƯU TẬP TIN TRONG THƯ MỤC NGƯỜI DÙNG (Không bao gồm thư mục và file log)
echo "--- ĐANG SAO LƯU TẬP TIN NGƯỜI DÙNG ---"
mkdir -p $TMP_DIR/user_files
# Tìm các file (không phải thư mục), không chứa 'log' trong tên, nằm trực tiếp trong PARENT_DIR
find "$PARENT_DIR" -maxdepth 1 -type f ! -iname "*log*" -exec cp {} "$TMP_DIR/user_files/" \; 2>/dev/null

# 6. ĐÓNG GÓI TẤT CẢ (Dữ liệu Bot + Cấu hình hệ thống)
echo "--- ĐANG NÉN DỮ LIỆU ---"
sudo tar -czf $BACKUP_DIR/$FILENAME -C $PARENT_DIR $SOURCE_NAME full_system_info

# 7. ĐẨY LÊN GOOGLE DRIVE
echo "--- ĐANG TẢI LÊN GOOGLE DRIVE ---"
rclone copy $BACKUP_DIR/$FILENAME gdrive:OpenClaw_Backups

if [ $? -eq 0 ]; then
    echo "SAO LƯU TOÀN DIỆN THÀNH CÔNG!"
else
    echo "LỖI KHI TẢI LÊN DRIVE"
fi

# 8. DỌN DẸP
sudo rm -rf $TMP_DIR
find $BACKUP_DIR -type f -name "*.tar.gz" -mtime +7 -delete
