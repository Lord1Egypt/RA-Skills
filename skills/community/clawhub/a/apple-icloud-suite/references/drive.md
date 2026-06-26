## 💾 Part 2: iCloud Drive ✅ 已验证

### 浏览文件

```python
#!/usr/bin/env python3
import os
os.environ['icloud_china'] = '1'
from pyicloud import PyiCloudService

api = PyiCloudService('your@email.com', 'password', china_mainland=True)

# 处理双重认证...

# 列出根目录
drive = api.drive
for item in drive.dir():
    print(f'📂 {item}')

# 进入子目录
subfolder = drive['Downloads']
for item in subfolder.dir():
    print(f'  📄 {item}')
```

### 下载文件

```python
# 下载文件
file = drive['文件名.pdf']
with file.open(stream=True) as response:
    with open('本地文件.pdf', 'wb') as f:
        f.write(response.raw.read())
```

---

