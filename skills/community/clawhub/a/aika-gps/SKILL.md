# AIKA GPS Skill

ดึงข้อมูล GPS จากระบบ AIKA สำหรับติดตาม location ช่าง

## ความสามารถ

- ดูตำแหน่งช่างแบบ real-time
- หาช่างใกล้ที่สุดสำหรับงานใหม่
- คำนวณระยะทางและ ETA
- สร้าง geofence สำหรับติดตามงาน

## คำสั่งที่รองรับ

### ดูตำแหน่งช่าง
- "ช่างโต้อยู่ไหน"
- "ดูตำแหน่งช่างทั้งหมด"
- "เช็ค GPS รถช่าง"

### หาช่างใกล้ที่สุด
- "หาช่างใกล้ที่สุด [ที่อยู่ลูกค้า]"
- "ใครอยู่ใกล้อบต.สระคู"
- "มอบหมายงาน [ที่อยู่] ให้ช่างใกล้ที่สุด"

### คำนวณระยะทาง
- "ระยะทางจากช่างโต้ไป [ที่อยู่]"
- "ETA ถึงลูกค้า"

## การติดตั้ง

1. ใส่ Device ID ในไฟล์ `references/aika_config.json`
2. ติดตั้ง dependencies: `pip install requests beautifulsoup4`
3. Restart OpenClaw gateway

## Files

- `scripts/aika_gps.py` - Python script สำหรับดึงข้อมูล
- `references/aika_config.json` - Configuration file
- `references/technicians.json` - รายชื่อช่าง + Device ID

## Security

- Password และ session token เก็บแยกใน config file
- ไม่แสดงข้อมูลส่วนบุคคลใน logs
- ใช้ HTTPS เท่านั้น

## Examples

```
คุณโหน่ง: ช่างโต้อยู่ไหน
คอมโฟน: 📍 ช่างโต้ - ถนน 2046 ใกล้โรงเรียนเปญจรัฏฐ์
         🕐 อัปเดต: 19:42 (2 นาทีที่แล้ว)
         🚗 ความเร็ว: 0 km/h (จอด)

คุณโหน่ง: หาช่างใกล้ที่สุด อบต.สระคู
คอมโฟน: 🔍 กำลังค้นหา...
         ✅ ช่างโต้ - 2.3 km (ETA 8 นาที)
         ⭐ Skills: กล้องวงจรปิด ✓
```