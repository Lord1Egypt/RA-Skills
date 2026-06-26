## 📷 Part 1: 照片 (pyicloud) ✅ 已验证

### 列出相册

```python
#!/usr/bin/env python3
import os
os.environ['icloud_china'] = '1'
from pyicloud import PyiCloudService

api = PyiCloudService('your@email.com', 'password', china_mainland=True)

# 处理双重认证...

# 列出所有相册
photos = api.photos
print(f'相册数量: {len(photos.albums)}')

for album_name in photos.albums:
    print(f'📁 {album_name}')
```

### 列出照片

```python
# 获取照片库
library = photos.albums['Library']

# 列出最近的照片
for i, photo in enumerate(library.photos):
    if i >= 10: break
    print(f'📷 {photo.filename} | {photo.created}')
```

### 下载照片

```python
# 获取第一张照片
photo = next(iter(library.photos))
print(f'正在下载: {photo.filename}')

# 下载
download = photo.download()
with open(photo.filename, 'wb') as f:
    f.write(download.raw.read())

print(f'✅ 已保存: {photo.filename}')
```

### 使用 icloudpd 批量下载

```bash
# 安装
pip install icloudpd

# 下载所有照片 (中国大陆)
icloudpd --directory ~/Pictures/iCloud \
         --username your@email.com \
         --domain cn

# 下载最近 100 张
icloudpd -d ~/Pictures/iCloud -u your@email.com --recent 100

# 持续同步 (每小时)
icloudpd -d ~/Pictures/iCloud -u your@email.com --watch-with-interval 3600
```

---

