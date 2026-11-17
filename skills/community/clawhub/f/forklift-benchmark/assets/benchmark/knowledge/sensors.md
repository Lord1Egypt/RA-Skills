<!--
forklift-benchmark-v2 / knowledge/sensors.md
sensor failure modes & mitigation strategies for forklift embodied-AI
covers: LiDAR, Camera, Depth, IMU, QR/code, RTK-GNSS, Ultrasonic, Wheel odometry
-->
# 叉车传感器异常模式知识库 / Forklift Sensor Anomaly Knowledge Base

> 用途:Benchmark 中"故障注入"与"鲁棒性测试"的事实基线。
> 覆盖:LiDAR、相机、深度图、IMU、二维码 / 标签、RTK-GNSS、超声波、轮式里程计、毫米波雷达、货叉力传感器。
> 每种传感器:触发条件、典型表现、应对策略、Benchmark 注入接口。

---

## 1. 传感器总体配置 / Sensor Stack Overview

```
叉车典型传感器配置(2025 主流)
├── 1. 主激光雷达 (Primary LiDAR)
│   ├── 数量:1-2 个(顶置 + 后置)
│   ├── 型号:禾赛 AT128 / Pandar XT-32 / Velodyne VLP-16
│   ├── 角度:360°
│   ├── 角分辨率:0.1°-0.4°
│   └── 测距:120-200 m
│
├── 2. 深度相机 (Depth Camera)
│   ├── 数量:2-4 个(前 + 后 + 货叉端)
│   ├── 型号:Intel RealSense D455 / Stereolabs ZED 2i / Orbbec Gemini 2
│   ├── 分辨率:1280×720 @ 30fps
│   └── 测距:0.4-15 m
│
├── 3. RGB 相机 (RGB Camera)
│   ├── 数量:4-6 个(360° 环视)
│   ├── 型号:海康 / 大华 / Axis 工业相机
│   └── 分辨率:1920×1080 @ 30fps
│
├── 4. IMU (惯性测量单元)
│   ├── 型号:Inertial Labs / XSens / VectorNav
│   ├── 6DOF 或 9DOF
│   └── 漂移:<0.5°/h(战术级)
│
├── 5. RTK-GNSS
│   ├── 型号:Trimble BD982 / NovAtel OEM7
│   └── 精度:±2 cm + 1 ppm
│
├── 6. 轮式里程计
│   ├── 来源:电机编码器
│   └── 精度:±0.5% 行驶距离
│
├── 7. 超声波雷达
│   ├── 数量:4-8 个(车身边缘)
│   ├── 频率:40-58 kHz
│   └── 测距:0.2-5 m
│
├── 8. 毫米波雷达
│   ├── 数量:1-2 个(前向)
│   ├── 频率:77 GHz
│   └── 测距:0.2-200 m
│
└── 9. 属具传感器
    ├── 货叉力传感器(称重)
    ├── 门架倾角仪
    ├── 货叉接近开关
    └── 二维码 / RFID 标签读取器
```

---

## 2. LiDAR 异常模式 / LiDAR Failure Modes

### 2.1 雨雪噪点 / Rain/Snow Noise

| 项 | 内容 |
|------|------|
| 触发条件 | 降雨 ≥ 5 mm/h、降雪 ≥ 1 cm/h、雾能见度 < 100m |
| 典型表现 | 点云中混入大量"雪花"或"雨帘"点;距离图像素值突然跳变;前端障碍物检测产生大量误报 |
| 量化指标 | 噪点增加 30-300%,有效测距降低 30-50% |
| 影响范围 | 障碍物检测失真,可能误刹或漏检 |
| 应对策略 | (1) 时间窗口中值滤波(5-10 帧);(2) 强度阈值过滤(雨点强度 < 50);(3) 雨雪检测器联动降低车速;(4) 多传感器融合(毫米波 + 视觉);(5) 雨刷 + 加热镜面 |
| Benchmark 注入 | `inject_lidar_rain(intensity=0.3, density=0.5)` |

### 2.2 灰尘 / 粉尘遮挡 / Dust Occlusion

| 项 | 内容 |
|------|------|
| 触发条件 | 水泥厂、面粉厂、煤场、矿场 |
| 典型表现 | 点云出现"扇形盲区"或"黑洞";镜面积尘 |
| 量化指标 | 局部区域点云密度下降 50-90% |
| 应对策略 | (1) 定期清洁镜面(每班次);(2) 压缩空气吹扫装置;(3) 多 LiDAR 冗余;(4) 视觉融合补充 |
| Benchmark 注入 | `inject_lidar_dust(position=vec3, opacity=0.7)` |

### 2.3 镜面反射 / Specular Reflection

| 项 | 内容 |
|------|------|
| 触发条件 | 镜面金属、玻璃幕墙、镜面不锈钢、抛光地坪 |
| 典型表现 | 测距出现"假远点"(镜面反射回激光的能量被二次反射);或完全"无点" |
| 量化指标 | 5-20% 角度出现鬼影 |
| 应对策略 | (1) 多次回波处理(取首次回波);(2) 强度阈值(滤除二次回波);(3) 视觉/毫米波补充 |
| Benchmark 注入 | `inject_lidar_specular(material='mirror_steel', area=[x,y,w,h])` |

### 2.4 多机干扰 / Inter-LiDAR Interference

| 项 | 内容 |
|------|------|
| 触发条件 | 多个 AGV/叉车相距 < 10m,激光束互射 |
| 典型表现 | 噪点、距离跳变、局部点云丢失 |
| 量化指标 | 受干扰角度占 5-30% |
| 应对策略 | (1) 编码 + 时间分片(各车使用不同相位);(2) 随机扰动序列;(3) 干扰检测 + 视觉 fallback |
| Benchmark 注入 | `inject_lidar_interference(vehicles=2, distance=5)` |

### 2.5 货叉货物遮挡 / Load Occlusion

| 项 | 内容 |
|------|------|
| 触发条件 | 大型货物遮挡 LiDAR 部分 FOV |
| 典型表现 | 货物后方出现"空区",盲区增大 |
| 应对策略 | (1) 多 LiDAR 覆盖;(2) 360° 冗余 |
| Benchmark 注入 | `inject_lidar_occlusion(angular_range=[-30, -10], distance=2)` |

### 2.6 完全失效 / Total Failure

| 项 | 内容 |
|------|------|
| 触发条件 | 电源故障、连接线缆断裂、激光器烧毁 |
| 典型表现 | 点云完全消失,FOV 内无数据 |
| 应对策略 | (1) 健康监测(每秒自检);(2) 立即进入安全模式(降速 + 视觉 + 毫米波);(3) 远程报警 + 派维护 |
| Benchmark 注入 | `inject_lidar_fail()` |

---

## 3. 相机异常模式 / Camera Anomaly Modes

### 3.1 逆光 / Backlight

| 项 | 内容 |
|------|------|
| 触发条件 | 阳光直射(室外)或高对比度光照 |
| 典型表现 | 图像过曝,暗部细节丢失,目标检测漏报 |
| 量化指标 | 动态范围超 100dB 时损失 30-50% 细节 |
| 应对策略 | (1) HDR 模式(多帧合成);(2) 自动曝光(分块测光);(3) 偏振滤镜;(4) WDR 摄像头 |
| Benchmark 注入 | `inject_camera_backlight(direction='front', intensity=100000lux)` |

### 3.2 反光 / Reflection Glare

| 项 | 内容 |
|------|------|
| 触发条件 | 抛光金属表面、镜面、湿滑地坪反光 |
| 典型表现 | 局部高光,目标识别失败 |
| 应对策略 | (1) 偏振镜;(2) 多角度图像融合;(3) 深度图补充 |
| Benchmark 注入 | `inject_camera_glare(position, size)` |

### 3.3 雨滴 / 镜头沾水 / Lens Water Drop

| 项 | 内容 |
|------|------|
| 触发条件 | 雨天、起雾、镜头结露 |
| 典型表现 | 图像出现"水痕""模糊""光晕" |
| 应对策略 | (1) 雨刷 + 加热;(2) 疏水涂层;(3) 镜头加热膜;(4) 多帧去雨 |
| Benchmark 注入 | `inject_camera_raindrops(density=0.3)` |

### 3.4 低光 / 暗光 / Low Light

| 项 | 内容 |
|------|------|
| 触发条件 | 夜间、地下库、暗区(<10 lux) |
| 典型表现 | 图像噪点爆炸,目标检测召回率下降 |
| 量化指标 | < 1 lux 暗光下,普通相机几乎不可用 |
| 应对策略 | (1) 大光圈镜头;(2) 高感光 CMOS(sony IMX585 等);(3) IR 红外补光;(4) 热成像;(5) 长曝光 |
| Benchmark 注入 | `inject_camera_lowlight(lux=1)` |

### 3.5 运动模糊 / Motion Blur

| 项 | 内容 |
|------|------|
| 触发条件 | 高速行驶(>10 km/h)+ 短曝光 |
| 典型表现 | 图像横向拖影 |
| 量化指标 | 行驶 15 km/h + 1ms 曝光,模糊长度约 4 像素 |
| 应对策略 | (1) 全局快门 CMOS;(2) 提高曝光时间(配补光);(3) 运动补偿 |
| Benchmark 注入 | `inject_camera_motion_blur(speed=15km/h)` |

### 3.6 镜头污染 / 遮挡 / Dirt/Occlusion

| 项 | 内容 |
|------|------|
| 触发条件 | 粉尘、油污、飞虫、临时遮挡 |
| 典型表现 | 局部黑斑,部分图像不可用 |
| 应对策略 | (1) 自清洁喷嘴;(2) 多相机冗余;(3) 健康监测 |
| Benchmark 注入 | `inject_camera_dirt(region, opacity=0.8)` |

### 3.7 镜头色偏 / Color Cast

| 项 | 内容 |
|------|------|
| 触发条件 | 工厂照明(钠灯黄、LED 白炽偏色) |
| 典型表现 | 图像色温偏差,白平衡失效 |
| 应对策略 | (1) 自动白平衡;(2) 多相机标定;(3) 标定白板 |
| Benchmark 注入 | `inject_camera_colorcast(temperature=2500K)` |

---

## 4. 深度图异常 / Depth Image Anomaly

### 4.1 深度空洞 / Depth Hole

| 项 | 内容 |
|------|------|
| 触发条件 | 反光、黑色吸光物体(>10m)、透明物体(玻璃)、小尺寸物体(细杆) |
| 典型表现 | 深度图出现"黑像素"(无效值) |
| 量化指标 | 玻璃 80-95% 深度丢失,黑色吸光材料 50% 深度异常 |
| 应对策略 | (1) 深度补全(Depth Completion Network);(2) 多帧融合;(3) LiDAR + RGB 融合(稀疏补密集) |
| Benchmark 注入 | `inject_depth_hole(region, density=0.4)` |

### 4.2 深度跳变 / Depth Discontinuity

| 项 | 内容 |
|------|------|
| 触发条件 | 物体边缘、低纹理表面 |
| 典型表现 | 边缘深度跳变,影响抓取定位 |
| 应对策略 | 双目 + ToF 融合(提高边缘精度) |
| Benchmark 注入 | `inject_depth_jump(distance=0.5m, position=edge)` |

### 4.3 视差失效 / Stereo Match Failure

| 项 | 内容 |
|------|------|
| 触发条件 | 重复纹理、纯色表面、镜面 |
| 典型表现 | 整片深度图紊乱 |
| 应对策略 | (1) 结构光补充;(2) ToF 补充;(3) 学习型匹配 |
| Benchmark 注入 | `inject_stereo_failure(region)` |

### 4.4 多深度图对齐失败 / Multi-Depth Misalignment

| 项 | 内容 |
|------|------|
| 触发条件 | 标定漂移、温度变化、振动 |
| 典型表现 | 多相机深度图拼接处错位 |
| 应对策略 | 定期在线标定 + 温度补偿 |
| Benchmark 注入 | `inject_depth_misalign(offset=0.1m)` |

---

## 5. IMU 异常 / IMU Anomaly

### 5.1 漂移 / Drift

| 项 | 内容 |
|------|------|
| 触发条件 | 长时间运行、温度变化、振动 |
| 典型表现 | 累积姿态误差;位置积分误差越来越大 |
| 量化指标 | 战术级 IMU 漂移 < 0.5°/h;消费级 5-10°/h |
| 影响 | 长时间依靠 IMU 定位,误差累积 5-10m / 1h |
| 应对策略 | (1) 周期性 GNSS/LiDAR 重置;(2) 卡尔曼滤波融合;(3) 高质量 IMU |
| Benchmark 注入 | `inject_imu_drift(rate=5°/h, duration=600s)` |

### 5.2 振动噪声 / Vibration Noise

| 项 | 内容 |
|------|------|
| 触发条件 | 路面不平、门架振动、发动机(柴油) |
| 典型表现 | 角速度 / 加速度高频噪声 |
| 应对策略 | (1) 隔振安装;(2) 低通滤波;(3) 信号调理 |
| Benchmark 注入 | `inject_imu_vibration(amplitude=0.5g, freq=50Hz)` |

### 5.3 磁干扰 / Magnetic Disturbance

| 项 | 内容 |
|------|------|
| 触发条件 | 大电流(电池、电机)、金属环境 |
| 典型表现 | 磁力计方向失真 |
| 应对策略 | (1) 磁力计在线校准;(2) 不依赖磁力计(融合卫星 + 视觉) |
| Benchmark 注入 | `inject_imu_mag_disturb(field_strength=100uT)` |

### 5.4 温度漂移 / Temperature Drift

| 项 | 内容 |
|------|------|
| 触发条件 | 极端温度(-20°C / +50°C)、快速温变 |
| 典型表现 | 零偏变化 50-200% |
| 应对策略 | 温度补偿 + 内置加热 |
| Benchmark 注入 | `inject_imu_temp_drift(delta=20°C)` |

### 5.5 失锁 / Tracking Loss

| 项 | 内容 |
|------|------|
| 触发条件 | 高速运动(> 5g 加速度)、撞击 |
| 典型表现 | 输出全部为零或饱和 |
| 应对策略 | 冗余 IMU + 冲击缓冲 |
| Benchmark 注入 | `inject_imu_lost(duration=2s)` |

---

## 6. 二维码 / 标签异常 / QR / Tag Anomaly

### 6.1 二维码污损 / Dirty QR Code

| 项 | 内容 |
|------|------|
| 触发条件 | 油污、磨损、撕裂、墨迹 |
| 典型表现 | 读取失败 / 误读 |
| 应对策略 | (1) 多视角尝试;(2) IR 读取;(3) 二维码 + RFID 双备份 |
| Benchmark 注入 | `inject_qr_damaged(area, level=0.5)` |

### 6.2 标签错位 / Tag Misplacement

| 项 | 内容 |
|------|------|
| 触发条件 | 人工贴错、托盘错放 |
| 典型表现 | 读到的库位与实际不符 |
| 应对策略 | 读码后视觉二次校验 |
| Benchmark 注入 | `inject_qr_misplaced()` |

### 6.3 RFID 干扰 / RFID Interference

| 项 | 内容 |
|------|------|
| 触发条件 | 金属反射、多标签碰撞 |
| 典型表现 | 漏读、误读、串读 |
| 应对策略 | 防碰撞算法(ISO 18000-63)、多次读取 |
| Benchmark 注入 | `inject_rfid_interference()` |

### 6.4 反光标签 / Reflective Tag

| 项 | 内容 |
|------|------|
| 触发条件 | 高反光膜标签 |
| 典型表现 | 工业相机过曝,识别失败 |
| 应对策略 | 偏振 + 调光 |
| Benchmark 注入 | `inject_qr_reflective()` |

---

## 7. RTK-GNSS 异常 / GNSS Anomaly

### 7.1 多径效应 / Multipath

| 项 | 内容 |
|------|------| 
| 触发条件 | 仓库高墙、集装箱堆场、建筑物反射 |
| 典型表现 | 定位跳变、伪距残差异常 |
| 量化指标 | 误差 0.5-5m |
| 应对策略 | (1) 多频多模 GNSS;(2) 抑径板;(3) 视觉/LiDAR 补充 |
| Benchmark 注入 | `inject_gnss_multipath(distance=0.5m)` |

### 7.2 卫星数不足 / Satellite Insufficiency

| 项 | 内容 |
|------|------|
| 触发条件 | 室内、地下、高架遮挡 |
| 典型表现 | RTK 无法固定,定位回退到单点 / 差分 |
| 应对策略 | 切换到 LiDAR 定位 + 视觉 |
| Benchmark 注入 | `inject_gnss_few_sats(n=3)` |

### 7.3 电离层扰动 / Ionospheric Disturbance

| 项 | 内容 |
|------|------|
| 触发条件 | 太阳活动高、地磁暴 |
| 典型表现 | 定位跳变、固定解丢失 |
| 应对策略 | 多频接收(L1+L2+L5)、SBAS |
| Benchmark 注入 | `inject_gnss_ionospheric()` |

### 7.4 欺骗 / Spoofing(高级威胁)

| 项 | 内容 |
|------|------|
| 触发条件 | 恶意 RF 信号 |
| 应对策略 | 信号强度 + 多源融合 |
| Benchmark 注入 | `inject_gnss_spoofing()` |

---

## 8. 超声波雷达异常 / Ultrasonic Anomaly

### 8.1 串扰 / Crosstalk

| 项 | 内容 |
|------|------|
| 触发条件 | 多超声波同时触发,声波互扰 |
| 典型表现 | 误测距、漏检 |
| 应对策略 | 错开发射时序、码分多址 |
| Benchmark 注入 | `inject_usonic_crosstalk()` |

### 8.2 吸声材料 / Sound Absorbing Material

| 项 | 内容 |
|------|------|
| 触发条件 | 棉包、化纤、泡沫、软包 |
| 典型表现 | 回波强度低,测距失败 |
| 应对策略 | 配合视觉 / LiDAR |
| Benchmark 注入 | `inject_usonic_absorber(material='cotton')` |

### 8.3 表面倾斜 / Surface Tilt

| 项 | 内容 |
|------|------|
| 触发条件 | 斜面(>30°) |
| 典型表现 | 反射波偏离,信号丢失 |
| 应对策略 | 多角度布设 |
| Benchmark 注入 | `inject_usonic_tilt(angle=30°)` |

---

## 9. 毫米波雷达异常 / mmWave Radar Anomaly

### 9.1 多径反射 / Multipath

| 项 | 内容 |
|------|------|
| 触发条件 | 金属集装箱、货架 |
| 典型表现 | 鬼影、漏检 |
| 应对策略 | CFAR 检测 + 目标跟踪 |
| Benchmark 注入 | `inject_radar_multipath()` |

### 9.2 静止目标漏检 / Static Target Missing

| 项 | 内容 |
|------|------|
| 触发条件 | 货架底部、地锁、低矮障碍 |
| 典型表现 | 静止目标被滤波 |
| 应对策略 | 关闭 MTI 滤波 / 速度补偿 |
| Benchmark 注入 | `inject_radar_static_filter()` |

### 9.3 大雨衰减 / Rain Attenuation

| 项 | 内容 |
|------|------|
| 触发条件 | 暴雨 > 50 mm/h |
| 典型表现 | 距离缩短,信号衰减 |
| 量化指标 | 77GHz 在大雨中衰减 1-3 dB/km |
| 应对策略 | 与视觉融合 |
| Benchmark 注入 | `inject_radar_rain(rain_rate=50mm/h)` |

---

## 10. 轮式里程计异常 / Wheel Odometry Anomaly

### 10.1 轮胎打滑 / Wheel Slip

| 项 | 内容 |
|------|------|
| 触发条件 | 油污、积水、冰面、加速急转 |
| 典型表现 | 编码器计数 > 实际距离(空转);或 < 实际(抱死) |
| 量化指标 | 打滑率 5-50% |
| 应对策略 | (1) IMU + 视觉融合校正;(2) 限制打滑工况速度 |
| Benchmark 注入 | `inject_wheel_slip(rate=0.3)` |

### 10.2 轮胎变形 / Tire Deformation

| 项 | 内容 |
|------|------|
| 触发条件 | 长期重载、胎压不足、扁平比小 |
| 典型表现 | 滚动半径变小,距离累积偏差 |
| 应对策略 | 定期标定 + 胎压监测 |
| Benchmark 注入 | `inject_tire_deform(scale=0.95)` |

### 10.3 编码器失效 / Encoder Failure

| 项 | 内容 |
|------|------|
| 触发条件 | 灰尘、振动、线缆断 |
| 典型表现 | 信号中断,无里程 |
| 应对策略 | 冗余编码器 + IMU 积分 |
| Benchmark 注入 | `inject_encoder_fail()` |

### 10.4 胎压异常 / Tire Pressure

| 项 | 内容 |
|------|------|
| 触发条件 | 漏气、温度变化 |
| 典型表现 | 滚动半径变化,里程误差 |
| 应对策略 | 胎压监测 + 定期打气 |
| Benchmark 注入 | `inject_tpms(warn_level=0.7)` |

---

## 11. 货叉力传感器 / Fork Force Sensor

### 11.1 过载报警 / Overload Warning

| 项 | 内容 |
|------|------|
| 触发条件 | 载荷 > 110% 额定 |
| 典型表现 | 力值超限,系统报警 |
| 应对策略 | 立即停止起升,声光报警 |
| Benchmark 注入 | `inject_fork_overload(weight=3500)` |

### 11.2 零点漂移 / Zero Drift

| 项 | 内容 |
|------|------|
| 触发条件 | 温度变化、长时间使用 |
| 典型表现 | 空载读数偏离 0 |
| 应对策略 | 周期性去皮(Tare) |
| Benchmark 注入 | `inject_fork_drift(offset=20kg)` |

### 11.3 货叉碰撞 / Fork Impact

| 项 | 内容 |
|------|------|
| 触发条件 | 货叉撞击货架、托盘、地面 |
| 典型表现 | 力值瞬时尖峰 |
| 应对策略 | 设定阈值,触发后自动减速 |
| Benchmark 注入 | `inject_fork_impact(force=5000N)` |

---

## 12. 门架倾角仪 / Mast Inclinometer

### 12.1 零点漂移 / Zero Drift

| 项 | 内容 |
|------|------|
| 触发条件 | 振动、老化 |
| 典型表现 | 倾角读数偏离 |
| 应对策略 | 周期性自校准 |
| Benchmark 注入 | `inject_mast_drift(offset=0.5°)` |

### 12.2 安装松动 / Mounting Loose

| 项 | 内容 |
|------|------|
| 触发条件 | 长期振动、螺栓松动 |
| 典型表现 | 倾角值跳变 |
| 应对策略 | 定期紧固 + 健康监测 |
| Benchmark 注入 | `inject_mast_loose(noise=0.3°)` |

---

## 13. Benchmark 故障注入接口 / Benchmark Fault Injection API

```python
# 统一故障注入接口
class SensorFaultInjector:
    def inject_lidar_rain(self, intensity: float, density: float):
        """LiDAR 雨雪噪点"""
        pass

    def inject_lidar_dust(self, position, opacity: float):
        """LiDAR 粉尘遮挡"""
        pass

    def inject_camera_backlight(self, direction, intensity_lux: float):
        """相机逆光"""
        pass

    def inject_camera_lowlight(self, lux: float):
        """相机低光"""
        pass

    def inject_camera_raindrops(self, density: float):
        """相机雨滴"""
        pass

    def inject_depth_hole(self, region, density: float):
        """深度图空洞"""
        pass

    def inject_imu_drift(self, rate_deg_per_h: float, duration_s: float):
        """IMU 漂移"""
        pass

    def inject_imu_vibration(self, amplitude_g: float, freq_hz: float):
        """IMU 振动"""
        pass

    def inject_qr_damaged(self, area, level: float):
        """二维码污损"""
        pass

    def inject_gnss_multipath(self, distance_m: float):
        """GNSS 多径"""
        pass

    def inject_gnss_few_sats(self, n: int):
        """卫星数不足"""
        pass

    def inject_wheel_slip(self, rate: float):
        """轮胎打滑"""
        pass

    def inject_tire_deform(self, scale: float):
        """轮胎变形"""
        pass

    def inject_fork_overload(self, weight_kg: float):
        """货叉过载"""
        pass

    def inject_fork_impact(self, force_n: float):
        """货叉碰撞"""
        pass
```

---

## 14. Benchmark 测试场景设计 / Benchmark Test Scenario Design

### 14.1 单故障场景
- L1: LiDAR 雨雪 + 高速行驶
- L2: 相机逆光 + 室外作业
- L3: IMU 漂移 + 长时间无 GNSS
- L4: 深度图空洞 + 反光货物
- L5: 二维码污损 + 高速扫码

### 14.2 复合故障场景
- **C1 雨雪复合** — LiDAR 雨噪 + 相机雨滴 + 路面湿滑 + 轮胎打滑
- **C2 高位 + 故障** — 高位作业 + 振动 + 风扰
- **C3 室内外切换** — GPS 失锁 + LiDAR 多径 + 光照突变
- **C4 长隧道 / 桥下** — GPS 完全失效 + LiDAR 退化 + 仅 IMU + 视觉
- **C5 急停场景** — IMU 饱和 + 编码器打滑 + 视觉运动模糊
- **C6 满载 + 颠簸** — 货叉过载报警 + IMU 振动 + 深度跳变

### 14.3 鲁棒性评分
- **鲁棒性指标 R**:
  $$R = 1 - \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\text{事故} \mid \text{故障}_i]$$
- 0 = 每次故障都出事故,1 = 全部故障都安全处理
- Benchmark 中期望 R > 0.85

---

## 15. 应对策略对照表 / Mitigation Strategy Table

| 故障类型 | 一级策略 | 二级策略 | Benchmark 期望 |
|------|------|------|------|
| LiDAR 雨雪 | 时间窗中值滤波 | 强度阈值 + 视觉融合 | 误报 < 5% |
| 粉尘遮挡 | 定期清洁 | 多 LiDAR 冗余 | 漏检 < 2% |
| 相机逆光 | HDR | 偏振 + WDR | 识别召回 > 90% |
| 相机低光 | IR 补光 | 增大光圈 | 召回 > 85% |
| 深度空洞 | 深度补全 | LiDAR 融合 | 有效率 > 95% |
| IMU 漂移 | 卡尔曼滤波 | 周期性重置 | 误差 < 1m/h |
| 二维码污损 | 多视角 | IR 读取 | 读取率 > 95% |
| GNSS 多径 | 多频 | 视觉补充 | 误差 < 0.2m |
| 轮胎打滑 | IMU 融合 | 限速 | 误差 < 1% |
| 货叉过载 | 力传感器 | 报警停机 | 误报 < 1% |

---

> **版权 / Copyright**:本文件基于杨鹏飞 / 叉车技术老炮维护的 forklift-expert 技能整理,CC BY-NC 4.0 + 严禁商用附加条款。
