## 📱 Part 3: 查找设备 ✅ 已验证

### 列出所有设备

```python
#!/usr/bin/env python3
import os
os.environ['icloud_china'] = '1'
from pyicloud import PyiCloudService

api = PyiCloudService('your@email.com', 'password', china_mainland=True)

# 处理双重认证...

# 列出所有设备
print('📱 我的设备:')
for device in api.devices:
    print(f'  - {device}')
```

### 设备定位和操作

```python
# 获取特定设备
iphone = api.devices['iPhone']

# 获取位置
location = iphone.location()
print(f'位置: {location}')

# 播放声音
iphone.play_sound()

# 丢失模式
iphone.lost_device(number='123456789', message='请联系我')
```

---

