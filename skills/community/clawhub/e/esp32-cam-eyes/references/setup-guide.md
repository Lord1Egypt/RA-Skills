# ESP32-S3-CAM Setup Guide

> Complete tutorial from zero to first photo, including common pitfalls.
> Tested with Hiwonder ESP32-S3 AI Vision Module + GC2145 sensor.

---

## Hardware Info

- **Board**: Hiwonder ESP32-S3 AI Vision Module
- **Sensor**: **GC2145** (Galaxycore, 2MP, PID: 0x2145)
  - ⚠️ **Not OV5640!** Easy to misidentify — always verify PID
  - Max resolution: 1600x1200 (UXGA)
  - **No hardware JPEG encoding** — this is a chip-level limitation, not a firmware issue
- **SoC**: ESP32-S3 (QFN56) revision v0.2, dual-core 240MHz
- **Memory**: 8MB PSRAM (Octal, 80MHz)
- **Connection**: USB-Serial (CH340 chip), device path `/dev/cu.usbserial-XXXX`
- **WiFi**: 2.4GHz only (ESP32 hardware limitation). Your computer can stay on 5GHz — both bands share the same LAN on most routers.

### Pin Definitions (Hiwonder/Freenove Compatible)

```
PWDN  = -1    RESET = -1
XCLK  = 15    PCLK  = 13
SIOD  = 4     SIOC  = 5
VSYNC = 6     HREF  = 7
D0(Y2)= 11    D1(Y3)= 9
D2(Y4)= 8     D3(Y5)= 10
D4(Y6)= 12    D5(Y7)= 18
D6(Y8)= 17    D7(Y9)= 16
```

---

## Recommended Approach

**Arduino framework + PlatformIO + RGB565 VGA/XGA + software JPEG encoding**

### Performance Benchmarks

| Resolution | Size | File Size | Speed | Recommendation |
|------------|------|-----------|-------|----------------|
| QQVGA 160×120 | Tiny | ~4KB | ~6s | ❌ Too slow and blurry |
| VGA 640×480 | Medium | ~41KB | <1s | ✅ Good for fast capture |
| SVGA 800×600 | Medium-Large | ~61KB | ~1s | ✅ Decent |
| **XGA 1024×768** | **Large** | **~92KB** | **~1.5s** | **✅ Best balance** |
| SXGA 1280×1024 | Very Large | ~128KB | ~4s | ⚠️ A bit slow |
| UXGA 1600×1200 | Max | Fails | — | ❌ Software encoding can't handle it |

**Recommended: XGA (1024×768)** — sharp enough for person/pet/object recognition, completes in 1-2 seconds.

---

## Step-by-Step Setup

### Prerequisites

Install on macOS (or Linux equivalent):
- **PlatformIO CLI**: `pip3 install --break-system-packages platformio`
- **esptool**: `pip3 install --break-system-packages esptool` (PlatformIO bundles it, but standalone install is handy)
- **pyserial**: `pip3 install --break-system-packages pyserial` (for serial communication)

First PlatformIO build downloads the ESP32 toolchain (~1.5-2GB). Subsequent builds are fast.

### Step 1: Plug in the ESP32-CAM and find the device

```bash
ls /dev/cu.usb*
```

You should see something like `/dev/cu.usbserial-XXXX`. Note this path.

Optionally verify chip info:
```bash
esptool chip-id --port /dev/cu.usbserial-XXXX
```

### Step 2: Identify the sensor model

This is **critical** — different sensors require different firmware strategies.

```bash
python3 -c "
import serial, time
s = serial.Serial('/dev/cu.usbserial-XXXX', 115200, timeout=1)
s.dtr = False; s.rts = True; time.sleep(0.1); s.rts = False
time.sleep(5)
data = s.read(8192)
s.close()
print(data.decode('utf-8', errors='replace'))
"
```

Look for `Sensor PID` in the output:
- **0x2145** = GC2145 (2MP, no hardware JPEG) → use this guide
- **0x5640** = OV5640 (5MP, hardware JPEG) → use `PIXFORMAT_JPEG` directly
- **0x2640** = OV2640 (2MP, hardware JPEG) → use `PIXFORMAT_JPEG` directly

### Step 3: Create the PlatformIO project

```bash
mkdir -p ~/esp32cam/src
cd ~/esp32cam
```

#### platformio.ini

```ini
[env:esp32s3cam]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino
board_build.arduino.memory_type = qio_opi
board_build.psram = enabled
monitor_speed = 115200
upload_port = /dev/cu.usbserial-XXXX    ; ← replace with your actual device path
upload_speed = 460800
build_flags = 
    -DBOARD_HAS_PSRAM
```

> ⚠️ Use `upload_speed = 460800`. The 921600 default causes "Unable to verify flash chip connection" on many boards.

#### src/main.cpp

```cpp
#include "esp_camera.h"
#include <WiFi.h>
#include "esp_http_server.h"

const char* ssid = "YOUR_WIFI_SSID";        // ← replace with your 2.4GHz WiFi
const char* password = "YOUR_WIFI_PASSWORD"; // ← replace

// Hiwonder/Freenove ESP32-S3 CAM pin definitions
#define PWDN_GPIO_NUM  -1
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  15
#define SIOD_GPIO_NUM  4
#define SIOC_GPIO_NUM  5
#define Y9_GPIO_NUM    16
#define Y8_GPIO_NUM    17
#define Y7_GPIO_NUM    18
#define Y6_GPIO_NUM    12
#define Y5_GPIO_NUM    10
#define Y4_GPIO_NUM    8
#define Y3_GPIO_NUM    9
#define Y2_GPIO_NUM    11
#define VSYNC_GPIO_NUM 6
#define HREF_GPIO_NUM  7
#define PCLK_GPIO_NUM  13

httpd_handle_t camera_httpd = NULL;

static esp_err_t capture_handler(httpd_req_t *req) {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }
    if (fb->format == PIXFORMAT_JPEG) {
        httpd_resp_set_type(req, "image/jpeg");
        httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
        esp_err_t res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
        esp_camera_fb_return(fb);
        return res;
    }
    // GC2145 doesn't support hardware JPEG — use software encoding
    uint8_t *jpg_buf = NULL;
    size_t jpg_len = 0;
    bool ok = frame2jpg(fb, 80, &jpg_buf, &jpg_len);
    esp_camera_fb_return(fb);
    if (ok) {
        httpd_resp_set_type(req, "image/jpeg");
        httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
        esp_err_t res = httpd_resp_send(req, (const char *)jpg_buf, jpg_len);
        free(jpg_buf);
        return res;
    }
    httpd_resp_send_500(req);
    return ESP_FAIL;
}

static esp_err_t stream_handler(httpd_req_t *req) {
    camera_fb_t *fb = NULL;
    esp_err_t res = ESP_OK;
    char part_buf[128];
    httpd_resp_set_type(req, "multipart/x-mixed-replace;boundary=frame");
    while (true) {
        fb = esp_camera_fb_get();
        if (!fb) { res = ESP_FAIL; break; }
        uint8_t *buf = fb->buf;
        size_t len = fb->len;
        uint8_t *jpg_buf = NULL;
        bool need_free = false;
        if (fb->format != PIXFORMAT_JPEG) {
            size_t jpg_len = 0;
            if (!frame2jpg(fb, 60, &jpg_buf, &jpg_len)) {
                esp_camera_fb_return(fb);
                continue;
            }
            buf = jpg_buf;
            len = jpg_len;
            need_free = true;
        }
        size_t hlen = snprintf(part_buf, 128,
            "--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n", len);
        res = httpd_resp_send_chunk(req, part_buf, hlen);
        if (res == ESP_OK) res = httpd_resp_send_chunk(req, (const char *)buf, len);
        if (res == ESP_OK) res = httpd_resp_send_chunk(req, "\r\n", 2);
        if (need_free) free(jpg_buf);
        esp_camera_fb_return(fb);
        if (res != ESP_OK) break;
    }
    return res;
}

static esp_err_t index_handler(httpd_req_t *req) {
    const char* html =
        "<html><body style='margin:0;background:#000;display:flex;justify-content:center;align-items:center;height:100vh'>"
        "<div style='text-align:center'>"
        "<h1 style='color:#0ff;font-family:monospace'>ESP32-CAM &#128065;</h1>"
        "<img src='/stream' style='max-width:100%;border:2px solid #0ff'><br><br>"
        "<a href='/capture' style='color:#0ff;font-family:monospace;font-size:1.2em'>Snapshot</a>"
        "</div></body></html>";
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, html, strlen(html));
}

void startCameraServer() {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.server_port = 80;
    if (httpd_start(&camera_httpd, &config) == ESP_OK) {
        httpd_uri_t u1 = { .uri = "/", .method = HTTP_GET, .handler = index_handler };
        httpd_uri_t u2 = { .uri = "/capture", .method = HTTP_GET, .handler = capture_handler };
        httpd_uri_t u3 = { .uri = "/stream", .method = HTTP_GET, .handler = stream_handler };
        httpd_register_uri_handler(camera_httpd, &u1);
        httpd_register_uri_handler(camera_httpd, &u2);
        httpd_register_uri_handler(camera_httpd, &u3);
    }
}

void setup() {
    Serial.begin(115200);
    Serial.println("\n\n=== ESP32-CAM Starting ===");

    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.grab_mode = CAMERA_GRAB_LATEST;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    
    // Try JPEG first (works if sensor supports it)
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 12;
    config.fb_count = 2;
    
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("JPEG failed (0x%x), falling back to RGB565 XGA...\n", err);
        // GC2145 doesn't support JPEG — fall back to RGB565
        config.pixel_format = PIXFORMAT_RGB565;
        config.frame_size = FRAMESIZE_XGA;  // 1024x768
        config.fb_count = 2;
        config.fb_location = CAMERA_FB_IN_PSRAM;
        err = esp_camera_init(&config);
    }
    
    if (err != ESP_OK) {
        Serial.printf("Camera init FAILED: 0x%x\n", err);
        return;
    }
    
    sensor_t *s = esp_camera_sensor_get();
    Serial.printf("Camera OK! PID=0x%x\n", s->id.PID);
    
    WiFi.begin(ssid, password);
    Serial.printf("Connecting to WiFi: %s", ssid);
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 30) {
        delay(500); Serial.print("."); attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.printf("\nWiFi connected! IP: %s\n", WiFi.localIP().toString().c_str());
        startCameraServer();
        Serial.printf("Camera ready! http://%s/capture\n", WiFi.localIP().toString().c_str());
    } else {
        Serial.println("\nWiFi connection failed! Starting AP mode...");
        WiFi.softAP("ESP32-CAM", "12345678");
        startCameraServer();
        Serial.printf("AP mode: http://%s/capture\n", WiFi.softAPIP().toString().c_str());
    }
}

void loop() { delay(10000); }
```

### Step 4: Build and flash

```bash
cd ~/esp32cam
pio run -t upload
```

First build downloads the toolchain (~1.5-2GB). After that, builds are near-instant. Flashing takes ~20 seconds.

### Step 5: Verify startup

```bash
python3 -c "
import serial, time
s = serial.Serial('/dev/cu.usbserial-XXXX', 115200, timeout=1)
s.dtr = False; s.rts = True; time.sleep(0.1); s.rts = False
time.sleep(15)
data = s.read(16384)
s.close()
print(data.decode('utf-8', errors='replace'))
"
```

Expected output:
```
=== ESP32-CAM Starting ===
Camera OK! PID=0x2145
WiFi connected! IP: 192.168.x.x
Camera ready! http://192.168.x.x/capture
```

### Step 6: Take a photo!

```bash
curl -m 15 -o /tmp/photo.jpg http://192.168.x.x/capture
```

Open `http://192.168.x.x/` in a browser to see the live MJPEG stream.

---

## API Endpoints

| Path | Function | Notes |
|------|----------|-------|
| `/` | Web UI | Displays live stream + snapshot link |
| `/capture` | Single snapshot | Returns JPEG image |
| `/stream` | MJPEG live stream | Note: GC2145 software encoding = low frame rate |

---

## Troubleshooting

### 1. Wrong sensor identification
**Problem**: PID 0x2145 mistaken for OV5640.
**Lesson**: Always check PID first. Common sensor PIDs:
- 0x2640 = OV2640 (supports JPEG ✅)
- 0x5640 = OV5640 (supports JPEG ✅)
- 0x2145 = GC2145 (no JPEG support ❌)

### 2. "JPEG format is not supported on this sensor"
**Problem**: Initializing GC2145 with `PIXFORMAT_JPEG` fails.
**Cause**: GC2145 hardware cannot encode JPEG. Must use RGB565 + software `frame2jpg()`.
**Fix**: Try JPEG first, fall back to RGB565 on failure (as shown in the firmware above).

### 3. Flash upload fails at high baud rate
**Problem**: Default 921600 baud rate causes "Unable to verify flash chip connection".
**Fix**: Use `upload_speed = 460800` in platformio.ini.

### 4. Factory firmware has no WiFi config UI
**Problem**: Hiwonder factory firmware creates an AP hotspot but the web server only starts after STA connection succeeds — no config page in AP mode.
**Fix**: Flash custom firmware directly.

### 5. QQVGA is slower than VGA (counter-intuitive)
**Problem**: QQVGA (160×120) takes ~6 seconds while VGA (<1 second).
**Cause**: Likely related to PSRAM DMA buffer efficiency — very small frames are less efficient.
**Lesson**: Don't assume smaller = faster. Benchmark your target resolution.

### 6. arduino-cli download failures
**Problem**: arduino-cli downloads of ESP32 toolchain (307MB+) fail repeatedly on unstable networks.
**Fix**: Use PlatformIO instead — more robust download management.

### 7. ESP-IDF framework complexity
**Problem**: ESP-IDF may offer better sensor support but has a complex build environment.
**Recommendation**: Stick with Arduino framework. If you have OV2640/OV5640 boards, Arduino supports hardware JPEG natively — no need for ESP-IDF.

---

## Purchasing Advice

If you haven't bought a board yet, prioritize boards with **OV2640** sensors. Hardware JPEG support means dramatically faster capture and higher resolution.

---

## Multi-Camera Deployment

Multiple ESP32-CAMs can join the same WiFi for multi-angle coverage:
- Bind fixed IPs via router DHCP reservation (by MAC address) to prevent IP changes on reboot
- Alternatively, use mDNS for service discovery
- Each camera uses the exact same firmware — just change the WiFi credentials
