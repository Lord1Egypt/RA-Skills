# Embedded Engineer — Code Examples

## Example 1

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>
#include <esp_task_wdt.h>
#include <SPIFFS.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <esp_ota_ops.h>
#include <HTTPUpdate.h>

// Advanced ESP32 IoT Sensor Hub with OTA, Web Interface, and Edge Processing

#define DEVICE_ID "ESP32_SENSOR_001"
#define FIRMWARE_VERSION "2.0.0"

// Hardware Configuration
#define BME280_I2C_ADDR 0x76
#define LED_STATUS 2
#define BUTTON_PIN 0
#define BATTERY_PIN 34

// Network Configuration
const char* ssid = "IoT_Network";
const char* password = "SecurePassword123";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;

// Timing Configuration
const unsigned long SENSOR_INTERVAL = 30000;  // 30 seconds
const unsigned long MQTT_RECONNECT_INTERVAL = 5000;
const unsigned long WDT_TIMEOUT = 30;  // 30 seconds

// Objects
WiFiClient espClient;
PubSubClient mqtt(espClient);
Adafruit_BME280 bme;
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

// State Management
struct SensorData {
    float temperature;
    float humidity;
    float pressure;
    float altitude;
    int batteryLevel;
    unsigned long timestamp;
    bool anomaly;
};

class EdgeProcessor {
private:
    static const int BUFFER_SIZE = 100;
    float tempBuffer[BUFFER_SIZE];
    int bufferIndex = 0;
    float movingAverage = 0;
    float stdDeviation = 0;
    
public:
    void addSample(float value) {
        tempBuffer[bufferIndex % BUFFER_SIZE] = value;
        bufferIndex++;
        
        if (bufferIndex >= BUFFER_SIZE) {
            calculateStatistics();
        }
    }
    
    void calculateStatistics() {
        float sum = 0, sumSquared = 0;
        
        for (int i = 0; i < BUFFER_SIZE; i++) {
            sum += tempBuffer[i];
            sumSquared += tempBuffer[i] * tempBuffer[i];
        }
        
        movingAverage = sum / BUFFER_SIZE;
        float variance = (sumSquared / BUFFER_SIZE) - (movingAverage * movingAverage);
        stdDeviation = sqrt(variance);
    }
    
    bool detectAnomaly(float value) {
        if (bufferIndex < BUFFER_SIZE) return false;
        return abs(value - movingAverage) > (3 * stdDeviation);
    }
    
    float getMovingAverage() { return movingAverage; }
    float getStdDeviation() { return stdDeviation; }
};

EdgeProcessor tempProcessor;
SensorData currentData;
SemaphoreHandle_t dataMutex;
QueueHandle_t eventQueue;

// Task Handles
TaskHandle_t sensorTaskHandle;
TaskHandle_t networkTaskHandle;
TaskHandle_t processingTaskHandle;

// OTA Update Handler
class OTAHandler {
private:
    bool updateInProgress = false;
    
public:
    void checkForUpdate() {
        if (updateInProgress) return;
        
        HTTPClient http;
        http.begin("http://update.server.com/firmware/latest.json");
        int httpCode = http.GET();
        
        if (httpCode == HTTP_CODE_OK) {
            DynamicJsonDocument doc(1024);
            DeserializationError error = deserializeJson(doc, http.getStream());
            
            if (!error) {
                const char* latestVersion = doc["version"];
                const char* updateUrl = doc["url"];
                
                if (strcmp(latestVersion, FIRMWARE_VERSION) > 0) {
                    performUpdate(updateUrl);
                }
            }
        }
        
        http.end();
    }
    
    void performUpdate(const char* url) {
        updateInProgress = true;
        
        WiFiClient client;
        t_httpUpdate_return ret = httpUpdate.update(client, url);
        
        switch(ret) {
            case HTTP_UPDATE_FAILED:
                Serial.printf("Update failed: %s\n", httpUpdate.getLastErrorString().c_str());
                break;
                
            case HTTP_UPDATE_NO_UPDATES:
                Serial.println("No updates available");
                break;
                
            case HTTP_UPDATE_OK:
                Serial.println("Update successful, restarting...");
                ESP.restart();
                break;
        }
        
        updateInProgress = false;
    }
};

OTAHandler otaHandler;

// Power Management
class PowerManager {
private:
    enum PowerMode {
        NORMAL,
        LOW_POWER,
        DEEP_SLEEP
    };
    
    PowerMode currentMode = NORMAL;
    int batteryThresholdLow = 20;
    int batteryThresholdCritical = 10;
    
public:
    void updatePowerMode(int batteryLevel) {
        if (batteryLevel < batteryThresholdCritical) {
            enterDeepSleep();
        } else if (batteryLevel < batteryThresholdLow) {
            enterLowPowerMode();
        } else {
            enterNormalMode();
        }
    }
    
    void enterNormalMode() {
        if (currentMode == NORMAL) return;
        
        currentMode = NORMAL;
        setCpuFrequencyMhz(240);
        WiFi.setSleep(false);
        Serial.println("Entering normal power mode");
    }
    
    void enterLowPowerMode() {
        if (currentMode == LOW_POWER) return;
        
        currentMode = LOW_POWER;
        setCpuFrequencyMhz(80);
        WiFi.setSleep(true);
        Serial.println("Entering low power mode");
    }
    
    void enterDeepSleep() {
        Serial.println("Entering deep sleep for 5 minutes");
        esp_sleep_enable_timer_wakeup(300 * 1000000);  // 5 minutes
        esp_deep_sleep_start();
    }
    
    int readBatteryLevel() {
        int raw = analogRead(BATTERY_PIN);
        float voltage = (raw / 4095.0) * 3.3 * 2;  // Assuming voltage divider
        return map(voltage * 100, 320, 420, 0, 100);  // 3.2V to 4.2V
    }
};

PowerManager powerManager;

// Sensor Task - Runs on Core 0
void sensorTask(void* parameter) {
    TickType_t xLastWakeTime = xTaskGetTickCount();
    
    while (true) {
        esp_task_wdt_reset();
        
        if (xSemaphoreTake(dataMutex, portMAX_DELAY)) {
            // Read sensor data
            currentData.temperature = bme.readTemperature();
            currentData.humidity = bme.readHumidity();
            currentData.pressure = bme.readPressure() / 100.0F;
            currentData.altitude = bme.readAltitude(1013.25);
            currentData.batteryLevel = powerManager.readBatteryLevel();
            currentData.timestamp = millis();
            
            // Edge processing
            tempProcessor.addSample(currentData.temperature);
            currentData.anomaly = tempProcessor.detectAnomaly(currentData.temperature);
            
            xSemaphoreGive(dataMutex);
            
            // Send event if anomaly detected
            if (currentData.anomaly) {
                EventData event = {EVENT_ANOMALY, currentData.temperature};
                xQueueSend(eventQueue, &event, 0);
            }
        }
        
        vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(SENSOR_INTERVAL));
    }
}

// Network Task - Runs on Core 1
void networkTask(void* parameter) {
    unsigned long lastMqttReconnect = 0;
    unsigned long lastPublish = 0;
    
    while (true) {
        esp_task_wdt_reset();
        
        // Maintain WiFi connection
        if (WiFi.status() != WL_CONNECTED) {
            connectWiFi();
        }
        
        // Maintain MQTT connection
        if (!mqtt.connected() && millis() - lastMqttReconnect > MQTT_RECONNECT_INTERVAL) {
            reconnectMQTT();
            lastMqttReconnect = millis();
        }
        
        // Publish sensor data
        if (mqtt.connected() && millis() - lastPublish > SENSOR_INTERVAL) {
            publishSensorData();
            lastPublish = millis();
        }
        
        mqtt.loop();
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

// Processing Task - Advanced Analytics
void processingTask(void* parameter) {
    EventData event;
    
    while (true) {
        if (xQueueReceive(eventQueue, &event, portMAX_DELAY)) {
            switch(event.type) {
                case EVENT_ANOMALY:
                    handleAnomaly(event);
                    break;
                case EVENT_THRESHOLD:
                    handleThreshold(event);
                    break;
                case EVENT_COMMAND:
                    handleCommand(event);
                    break;
            }
        }
    }
}

void connectWiFi() {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi connected");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("\nWiFi connection failed");
    }
}

void reconnectMQTT() {
    if (mqtt.connect(DEVICE_ID)) {
        Serial.println("MQTT connected");
        
        // Subscribe to command topics
        mqtt.subscribe("iot/devices/ESP32_SENSOR_001/commands");
        mqtt.subscribe("iot/devices/ESP32_SENSOR_001/config");
        mqtt.subscribe("iot/broadcast/firmware");
        
        // Publish online status
        StaticJsonDocument<256> doc;
        doc["device_id"] = DEVICE_ID;
        doc["status"] = "online";
        doc["firmware"] = FIRMWARE_VERSION;
        doc["ip"] = WiFi.localIP().toString();
        
        char buffer[256];
        serializeJson(doc, buffer);
        mqtt.publish("iot/devices/ESP32_SENSOR_001/status", buffer, true);
    }
}

void publishSensorData() {
    if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(100))) {
        StaticJsonDocument<512> doc;
        
        doc["device_id"] = DEVICE_ID;
        doc["timestamp"] = currentData.timestamp;
        
        JsonObject sensors = doc.createNestedObject("sensors");
        sensors["temperature"] = currentData.temperature;
        sensors["humidity"] = currentData.humidity;
        sensors["pressure"] = currentData.pressure;
        sensors["altitude"] = currentData.altitude;
        
        JsonObject analytics = doc.createNestedObject("analytics");
        analytics["temp_avg"] = tempProcessor.getMovingAverage();
        analytics["temp_std"] = tempProcessor.getStdDeviation();
        analytics["anomaly"] = currentData.anomaly;
        
        JsonObject system = doc.createNestedObject("system");
        system["battery"] = currentData.batteryLevel;
        system["free_heap"] = ESP.getFreeHeap();
        system["uptime"] = millis();
        
        char buffer[512];
        serializeJson(doc, buffer);
        
        mqtt.publish("iot/devices/ESP32_SENSOR_001/telemetry", buffer);
        
        // Also send to WebSocket clients
        ws.textAll(buffer);
        
        xSemaphoreGive(dataMutex);
    }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, payload, length);
    
    if (error) {
        Serial.print("JSON parse error: ");
        Serial.println(error.c_str());
        return;
    }
    
    if (strcmp(topic, "iot/devices/ESP32_SENSOR_001/commands") == 0) {
        const char* command = doc["command"];
        
        if (strcmp(command, "restart") == 0) {
            ESP.restart();
        } else if (strcmp(command, "update") == 0) {
            otaHandler.checkForUpdate();
        } else if (strcmp(command, "calibrate") == 0) {
            calibrateSensors();
        }
    }
}

// Web Server Handlers
void setupWebServer() {
    // Serve static files from SPIFFS
    server.serveStatic("/", SPIFFS, "/www/").setDefaultFile("index.html");
    
    // API endpoints
    server.on("/api/data", HTTP_GET, [](AsyncWebServerRequest *request) {
        if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(100))) {
            StaticJsonDocument<512> doc;
            doc["temperature"] = currentData.temperature;
            doc["humidity"] = currentData.humidity;
            doc["pressure"] = currentData.pressure;
            doc["battery"] = currentData.batteryLevel;
            
            String response;
            serializeJson(doc, response);
            
            xSemaphoreGive(dataMutex);
            
            request->send(200, "application/json", response);
        } else {
            request->send(503, "application/json", "{\"error\":\"Data unavailable\"}");
        }
    });
    
    server.on("/api/config", HTTP_POST, [](AsyncWebServerRequest *request) {
        // Handle configuration updates
    });
    
    // WebSocket event handler
    ws.onEvent(onWsEvent);
    server.addHandler(&ws);
    
    server.begin();
}

void onWsEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, 
               AwsEventType type, void *arg, uint8_t *data, size_t len) {
    switch(type) {
        case WS_EVT_CONNECT:
            Serial.printf("WebSocket client #%u connected\n", client->id());
            break;
            
        case WS_EVT_DISCONNECT:
            Serial.printf("WebSocket client #%u disconnected\n", client->id());
            break;
            
        case WS_EVT_DATA:
            // Handle incoming WebSocket data
            break;
    }
}

void setup() {
    Serial.begin(115200);
    
    // Initialize mutex and queue
    dataMutex = xSemaphoreCreateMutex();
    eventQueue = xQueueCreate(10, sizeof(EventData));
    
    // Initialize I2C
    Wire.begin();
    
    // Initialize sensors
    if (!bme.begin(BME280_I2C_ADDR)) {
        Serial.println("BME280 sensor not found!");
    }
    
    // Initialize SPIFFS
    if (!SPIFFS.begin(true)) {
        Serial.println("SPIFFS mount failed");
    }
    
    // Configure watchdog
    esp_task_wdt_init(WDT_TIMEOUT, true);
    esp_task_wdt_add(NULL);
    
    // Setup WiFi
    WiFi.mode(WIFI_STA);
    connectWiFi();
    
    // Setup MQTT
    mqtt.setServer(mqtt_server, mqtt_port);
    mqtt.setCallback(mqttCallback);
    mqtt.setBufferSize(1024);
    
    // Setup web server
    setupWebServer();
    
    // Create tasks on specific cores
    xTaskCreatePinnedToCore(
        sensorTask,
        "SensorTask",
        4096,
        NULL,
        1,
        &sensorTaskHandle,
        0  // Core 0
    );
    
    xTaskCreatePinnedToCore(
        networkTask,
        "NetworkTask",
        8192,
        NULL,
        1,
        &networkTaskHandle,
        1  // Core 1
    );
    
    xTaskCreatePinnedToCore(
        processingTask,
        "ProcessingTask",
        4096,
        NULL,
        2,
        &processingTaskHandle,
        1  // Core 1
    );
    
    Serial.println("ESP32 IoT Sensor Hub initialized");
}

void loop() {
    // Main loop kept minimal - all work done in tasks
    esp_task_wdt_reset();
    
    // Check for button press
    static unsigned long lastButtonPress = 0;
    if (digitalRead(BUTTON_PIN) == LOW && millis() - lastButtonPress > 1000) {
        lastButtonPress = millis();
        
        // Triple press for factory reset
        static int pressCount = 0;
        static unsigned long firstPressTime = 0;
        
        if (millis() - firstPressTime > 3000) {
            pressCount = 0;
            firstPressTime = millis();
        }
        
        pressCount++;
        
        if (pressCount >= 3) {
            factoryReset();
        }
    }
    
    // Periodic OTA check (once per hour)
    static unsigned long lastOTACheck = 0;
    if (millis() - lastOTACheck > 3600000) {
        otaHandler.checkForUpdate();
        lastOTACheck = millis();
    }
    
    delay(100);
}

void factoryReset() {
    Serial.println("Factory reset initiated");
    
    // Clear SPIFFS
    SPIFFS.format();
    
    // Clear WiFi credentials
    WiFi.disconnect(true);
    
    // Restart
    ESP.restart();
}
```

## Example 2

```python
#!/usr/bin/env python3
"""
Industrial IoT Gateway for Raspberry Pi
Supports multiple protocols, edge computing, and cloud connectivity
"""

import asyncio
import json
import time
import threading
import logging
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import struct
import queue

# Hardware interfaces
import RPi.GPIO as GPIO
import spidev
import serial
import smbus2

# Networking
import paho.mqtt.client as mqtt
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, modbus_rtu
import opcua
from opcua import Server, Client
import aiocoap
import websockets

# Edge AI
import tflite_runtime.interpreter as tflite
import cv2

# Cloud SDKs
from azure.iot.device.aio import IoTHubDeviceClient
import boto3
from google.cloud import iot_v1

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DeviceConfig:
    """Device configuration"""
    device_id: str
    location: str
    capabilities: List[str]
    protocols: List[str]
    cloud_provider: str
    edge_ai_enabled: bool
    
@dataclass
class SensorReading:
    """Sensor data structure"""
    sensor_id: str
    timestamp: float
    value: float
    unit: str
    quality: int
    metadata: Dict[str, Any]

class Protocol(Enum):
    """Communication protocols"""
    MODBUS_TCP = "modbus_tcp"
    MODBUS_RTU = "modbus_rtu"
    OPCUA = "opcua"
    MQTT = "mqtt"
    COAP = "coap"
    LORA = "lora"

class EdgeGateway:
    """Industrial IoT Edge Gateway"""
    
    def __init__(self, config: DeviceConfig):
        self.config = config
        self.running = False
        
        # Hardware setup
        GPIO.setmode(GPIO.BCM)
        self.spi = spidev.SpiDev()
        self.i2c = smbus2.SMBus(1)
        
        # Data management
        self.data_queue = queue.Queue(maxsize=10000)
        self.event_queue = queue.Queue(maxsize=1000)
        self.db_conn = self._init_database()
        
        # Protocol handlers
        self.protocol_handlers = {}
        self._init_protocols()
        
        # Edge AI
        if config.edge_ai_enabled:
            self.ai_engine = EdgeAIEngine()
        
        # Cloud connectivity
        self.cloud_client = self._init_cloud_client()
        
    def _init_database(self) -> sqlite3.Connection:
        """Initialize local database for buffering"""
        conn = sqlite3.connect('gateway_data.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                timestamp REAL NOT NULL,
                value REAL NOT NULL,
                unit TEXT,
                quality INTEGER,
                metadata TEXT,
                synced BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                source TEXT NOT NULL,
                message TEXT,
                data TEXT,
                acknowledged BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        return conn
    
    def _init_protocols(self):
        """Initialize protocol handlers"""
        if Protocol.MODBUS_TCP.value in self.config.protocols:
            self.protocol_handlers[Protocol.MODBUS_TCP] = ModbusTCPHandler()
        
        if Protocol.MODBUS_RTU.value in self.config.protocols:
            self.protocol_handlers[Protocol.MODBUS_RTU] = ModbusRTUHandler('/dev/ttyUSB0')
        
        if Protocol.OPCUA.value in self.config.protocols:
            self.protocol_handlers[Protocol.OPCUA] = OPCUAHandler()
        
        if Protocol.MQTT.value in self.config.protocols:
            self.protocol_handlers[Protocol.MQTT] = MQTTHandler()
        
        if Protocol.LORA.value in self.config.protocols:
            self.protocol_handlers[Protocol.LORA] = LoRaHandler()
    
    def _init_cloud_client(self):
        """Initialize cloud client based on provider"""
        if self.config.cloud_provider == "azure":
            return AzureIoTClient(self.config.device_id)
        elif self.config.cloud_provider == "aws":
            return AWSIoTClient(self.config.device_id)
        elif self.config.cloud_provider == "gcp":
            return GCPIoTClient(self.config.device_id)
        else:
            return None

class ModbusTCPHandler:
    """Modbus TCP protocol handler"""
    
    def __init__(self, host='0.0.0.0', port=502):
        self.master = modbus_tcp.TcpMaster(host, port)
        self.master.set_timeout(5.0)
        
    async def read_registers(self, slave_id: int, start_addr: int, 
                            count: int) -> List[int]:
        """Read holding registers"""
        try:
            return self.master.execute(
                slave_id, 
                cst.READ_HOLDING_REGISTERS, 
                start_addr, 
                count
            )
        except Exception as e:
            logger.error(f"Modbus read error: {e}")
            return []
    
    async def write_register(self, slave_id: int, addr: int, value: int):
        """Write single register"""
        try:
            self.master.execute(
                slave_id,
                cst.WRITE_SINGLE_REGISTER,
                addr,
                output_value=value
            )
        except Exception as e:
            logger.error(f"Modbus write error: {e}")

class ModbusRTUHandler:
    """Modbus RTU protocol handler"""
    
    def __init__(self, port: str, baudrate: int = 9600):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1
        )
        self.master = modbus_rtu.RtuMaster(self.serial)
        self.master.set_timeout(5.0)
        
    def read_input_registers(self, slave_id: int, start_addr: int, 
                            count: int) -> List[int]:
        """Read input registers"""
        try:
            return self.master.execute(
                slave_id,
                cst.READ_INPUT_REGISTERS,
                start_addr,
                count
            )
        except Exception as e:
            logger.error(f"Modbus RTU error: {e}")
            return []

class OPCUAHandler:
    """OPC UA protocol handler"""
    
    def __init__(self):
        self.server = Server()
        self.server.set_endpoint("opc.tcp://0.0.0.0:4840")
        self.server.set_server_name("Industrial IoT Gateway")
        
        # Setup namespace
        uri = "http://industrial.iot.gateway"
        self.idx = self.server.register_namespace(uri)
        
        # Create objects
        self.objects = self.server.get_objects_node()
        self.device = self.objects.add_object(self.idx, "Gateway")
        
    async def start(self):
        """Start OPC UA server"""
        self.server.start()
        logger.info("OPC UA server started")
        
    async def add_variable(self, name: str, value: Any) -> opcua.Node:
        """Add a variable to the server"""
        var = self.device.add_variable(self.idx, name, value)
        var.set_writable()
        return var
    
    async def update_variable(self, node: opcua.Node, value: Any):
        """Update variable value"""
        node.set_value(value)

class MQTTHandler:
    """MQTT protocol handler with QoS and persistence"""
    
    def __init__(self, broker: str = "localhost", port: int = 1883):
        self.client = mqtt.Client(client_id=f"gateway_{int(time.time())}")
        self.broker = broker
        self.port = port
        self.connected = False
        
        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        # Message buffer for offline operation
        self.message_buffer = []
        
    def _on_connect(self, client, userdata, flags, rc):
        """Connection callback"""
        if rc == 0:
            self.connected = True
            logger.info("MQTT connected")
            
            # Flush buffered messages
            for msg in self.message_buffer:
                self.publish(msg['topic'], msg['payload'], msg['qos'])
            self.message_buffer.clear()
        else:
            logger.error(f"MQTT connection failed: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Disconnection callback"""
        self.connected = False
        logger.warning("MQTT disconnected")
        
    def _on_message(self, client, userdata, msg):
        """Message callback"""
        try:
            payload = json.loads(msg.payload.decode())
            logger.info(f"MQTT message received: {msg.topic}")
            # Process message
        except Exception as e:
            logger.error(f"MQTT message error: {e}")
    
    async def connect(self):
        """Connect to broker"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT connection error: {e}")
    
    def publish(self, topic: str, payload: Dict, qos: int = 1):
        """Publish message with QoS"""
        if self.connected:
            self.client.publish(
                topic,
                json.dumps(payload),
                qos=qos,
                retain=False
            )
        else:
            # Buffer for later
            self.message_buffer.append({
                'topic': topic,
                'payload': payload,
                'qos': qos
            })

class LoRaHandler:
    """LoRa/LoRaWAN handler for long-range communication"""
    
    def __init__(self, spi_bus: int = 0, spi_device: int = 0):
        # LoRa module configuration (e.g., SX1276)
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 50000
        
        # GPIO pins
        self.RESET_PIN = 17
        self.DIO0_PIN = 4
        
        GPIO.setup(self.RESET_PIN, GPIO.OUT)
        GPIO.setup(self.DIO0_PIN, GPIO.IN)
        
        self._init_lora()
    
    def _init_lora(self):
        """Initialize LoRa module"""
        # Reset module
        GPIO.output(self.RESET_PIN, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self.RESET_PIN, GPIO.HIGH)
        time.sleep(0.01)
        
        # Configure registers
        self._write_register(0x01, 0x80)  # Sleep mode
        self._write_register(0x01, 0x81)  # LoRa mode
        
        # Set frequency (868 MHz)
        freq = int(868000000 / 61.035)
        self._write_register(0x06, (freq >> 16) & 0xFF)
        self._write_register(0x07, (freq >> 8) & 0xFF)
        self._write_register(0x08, freq & 0xFF)
        
        # Set spreading factor, bandwidth, coding rate
        self._write_register(0x1D, 0x72)  # SF7, BW125, CR4/5
        self._write_register(0x1E, 0x74)  # SF7, CRC on
        
    def _write_register(self, addr: int, value: int):
        """Write to LoRa register"""
        self.spi.xfer2([addr | 0x80, value])
        
    def _read_register(self, addr: int) -> int:
        """Read from LoRa register"""
        result = self.spi.xfer2([addr & 0x7F, 0x00])
        return result[1]
    
    def send_packet(self, data: bytes):
        """Send LoRa packet"""
        # Set to standby mode
        self._write_register(0x01, 0x81)
        
        # Set FIFO pointer
        self._write_register(0x0D, 0x80)
        
        # Write data to FIFO
        for byte in data:
            self._write_register(0x00, byte)
        
        # Set payload length
        self._write_register(0x22, len(data))
        
        # Start transmission
        self._write_register(0x01, 0x83)
        
        # Wait for transmission complete
        while not GPIO.input(self.DIO0_PIN):
            time.sleep(0.001)
    
    def receive_packet(self) -> Optional[bytes]:
        """Receive LoRa packet"""
        # Check for packet
        if GPIO.input(self.DIO0_PIN):
            # Get packet length
            length = self._read_register(0x13)
            
            # Set FIFO pointer
            current_addr = self._read_register(0x10)
            self._write_register(0x0D, current_addr)
            
            # Read packet
            packet = []
            for _ in range(length):
                packet.append(self._read_register(0x00))
            
            # Clear IRQ
            self._write_register(0x12, 0xFF)
            
            return bytes(packet)
        
        return None

class EdgeAIEngine:
    """Edge AI processing engine"""
    
    def __init__(self):
        self.models = {}
        self.load_models()
        
    def load_models(self):
        """Load TensorFlow Lite models"""
        # Anomaly detection model
        self.models['anomaly'] = tflite.Interpreter(
            model_path='/opt/models/anomaly_detection.tflite'
        )
        self.models['anomaly'].allocate_tensors()
        
        # Predictive maintenance model
        self.models['maintenance'] = tflite.Interpreter(
            model_path='/opt/models/predictive_maintenance.tflite'
        )
        self.models['maintenance'].allocate_tensors()
        
    def detect_anomaly(self, data: np.ndarray) -> Tuple[bool, float]:
        """Detect anomalies in sensor data"""
        interpreter = self.models['anomaly']
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        # Preprocess data
        input_data = np.array(data, dtype=np.float32).reshape(1, -1)
        
        # Run inference
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        
        # Get results
        output_data = interpreter.get_tensor(output_details[0]['index'])
        anomaly_score = float(output_data[0][0])
        
        return anomaly_score > 0.7, anomaly_score
    
    def predict_maintenance(self, sensor_history: np.ndarray) -> Dict[str, Any]:
        """Predict maintenance requirements"""
        interpreter = self.models['maintenance']
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        # Prepare input
        input_data = sensor_history.astype(np.float32).reshape(1, -1)
        
        # Run inference
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        
        # Get results
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        return {
            'failure_probability': float(output_data[0][0]),
            'estimated_days_to_failure': int(output_data[0][1]),
            'recommended_action': self._get_maintenance_action(output_data[0][2])
        }
    
    def _get_maintenance_action(self, action_code: int) -> str:
        """Map action code to recommendation"""
        actions = {
            0: "No action required",
            1: "Schedule routine maintenance",
            2: "Inspect component",
            3: "Replace component immediately"
        }
        return actions.get(action_code, "Unknown")

class DataProcessor:
    """Real-time data processing and aggregation"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.data_windows = {}
        
    def add_sample(self, sensor_id: str, value: float):
        """Add sample to processing window"""
        if sensor_id not in self.data_windows:
            self.data_windows[sensor_id] = []
        
        window = self.data_windows[sensor_id]
        window.append(value)
        
        if len(window) > self.window_size:
            window.pop(0)
    
    def calculate_statistics(self, sensor_id: str) -> Dict[str, float]:
        """Calculate statistics for sensor"""
        if sensor_id not in self.data_windows:
            return {}
        
        window = np.array(self.data_windows[sensor_id])
        
        return {
            'mean': np.mean(window),
            'std': np.std(window),
            'min': np.min(window),
            'max': np.max(window),
            'median': np.median(window),
            'trend': self._calculate_trend(window)
        }
    
    def _calculate_trend(self, data: np.ndarray) -> float:
        """Calculate trend using linear regression"""
        if len(data) < 2:
            return 0.0
        
        x = np.arange(len(data))
        coeffs = np.polyfit(x, data, 1)
        return coeffs[0]

# Main execution
async def main():
    """Main gateway execution"""
    config = DeviceConfig(
        device_id="RPI_GATEWAY_001",
        location="Factory Floor A",
        capabilities=["modbus", "opcua", "mqtt", "lora", "edge_ai"],
        protocols=["modbus_tcp", "opcua", "mqtt", "lora"],
        cloud_provider="azure",
        edge_ai_enabled=True
    )
    
    gateway = EdgeGateway(config)
    
    try:
        # Start gateway
        await gateway.start()
        
        # Run forever
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down gateway...")
        await gateway.stop()
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 3

```c
/**
 * STM32F4 Real-Time Industrial Control System
 * Bare-metal implementation with FreeRTOS
 */

#include "stm32f4xx.h"
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include "timers.h"
#include <string.h>
#include <math.h>

// Hardware Configuration
#define LED_PIN         GPIO_PIN_13
#define SENSOR_ADC_CH   ADC_CHANNEL_0
#define PWM_TIM         TIM2
#define UART_BAUDRATE   115200
#define CAN_BITRATE     500000

// Task Priorities
#define PRIORITY_CRITICAL   (configMAX_PRIORITIES - 1)
#define PRIORITY_HIGH       (configMAX_PRIORITIES - 2)
#define PRIORITY_NORMAL     (configMAX_PRIORITIES - 3)
#define PRIORITY_LOW        (configMAX_PRIORITIES - 4)

// System Configuration
typedef struct {
    uint32_t device_id;
    uint32_t sample_rate_hz;
    uint32_t control_period_ms;
    float setpoint;
    float kp, ki, kd;  // PID parameters
    uint8_t safety_enabled;
} SystemConfig_t;

// Sensor Data Structure
typedef struct {
    uint32_t timestamp;
    float temperature;
    float pressure;
    float flow_rate;
    float voltage;
    float current;
    uint8_t status;
} SensorData_t;

// Control Output
typedef struct {
    float pwm_duty;
    uint8_t relay_state;
    float valve_position;
    uint32_t error_code;
} ControlOutput_t;

// Global handles
static QueueHandle_t xSensorQueue;
static QueueHandle_t xControlQueue;
static SemaphoreHandle_t xI2CMutex;
static SemaphoreHandle_t xCANMutex;
static TimerHandle_t xWatchdogTimer;

// DMA buffers
__attribute__((aligned(4))) static uint16_t adc_dma_buffer[16];
__attribute__((aligned(4))) static uint8_t uart_rx_buffer[256];
__attribute__((aligned(4))) static uint8_t uart_tx_buffer[256];

// PID Controller
typedef struct {
    float kp, ki, kd;
    float integral;
    float prev_error;
    float output_min, output_max;
    uint32_t last_time;
} PIDController_t;

static PIDController_t pid_controller = {
    .kp = 2.0f,
    .ki = 0.5f,
    .kd = 0.1f,
    .output_min = 0.0f,
    .output_max = 100.0f
};

// Function prototypes
static void SystemClock_Config(void);
static void GPIO_Init(void);
static void ADC_Init(void);
static void UART_Init(void);
static void CAN_Init(void);
static void I2C_Init(void);
static void TIM_PWM_Init(void);
static void DMA_Init(void);
static void NVIC_Init(void);

// Task prototypes
static void vSensorTask(void *pvParameters);
static void vControlTask(void *pvParameters);
static void vCommunicationTask(void *pvParameters);
static void vSafetyTask(void *pvParameters);
static void vDiagnosticsTask(void *pvParameters);

// Interrupt handlers
void ADC_IRQHandler(void);
void DMA2_Stream0_IRQHandler(void);
void CAN1_RX0_IRQHandler(void);
void USART1_IRQHandler(void);
void TIM2_IRQHandler(void);

/**
 * Main entry point
 */
int main(void) {
    // Initialize HAL and system
    HAL_Init();
    SystemClock_Config();
    
    // Initialize peripherals
    GPIO_Init();
    ADC_Init();
    UART_Init();
    CAN_Init();
    I2C_Init();
    TIM_PWM_Init();
    DMA_Init();
    NVIC_Init();
    
    // Create FreeRTOS objects
    xSensorQueue = xQueueCreate(10, sizeof(SensorData_t));
    xControlQueue = xQueueCreate(5, sizeof(ControlOutput_t));
    xI2CMutex = xSemaphoreCreateMutex();
    xCANMutex = xSemaphoreCreateMutex();
    
    // Create watchdog timer
    xWatchdogTimer = xTimerCreate(
        "Watchdog",
        pdMS_TO_TICKS(1000),
        pdTRUE,
        NULL,
        vWatchdogCallback
    );
    
    // Create tasks
    xTaskCreate(vSensorTask, "Sensor", 512, NULL, PRIORITY_HIGH, NULL);
    xTaskCreate(vControlTask, "Control", 768, NULL, PRIORITY_CRITICAL, NULL);
    xTaskCreate(vCommunicationTask, "Comm", 1024, NULL, PRIORITY_NORMAL, NULL);
    xTaskCreate(vSafetyTask, "Safety", 256, NULL, PRIORITY_CRITICAL, NULL);
    xTaskCreate(vDiagnosticsTask, "Diag", 512, NULL, PRIORITY_LOW, NULL);
    
    // Start watchdog timer
    xTimerStart(xWatchdogTimer, 0);
    
    // Start scheduler
    vTaskStartScheduler();
    
    // Should never reach here
    while(1);
}

/**
 * Sensor acquisition task - runs every 10ms
 */
static void vSensorTask(void *pvParameters) {
    SensorData_t sensor_data;
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xPeriod = pdMS_TO_TICKS(10);
    
    for(;;) {
        // Wait for precise timing
        vTaskDelayUntil(&xLastWakeTime, xPeriod);
        
        // Read ADC channels via DMA
        HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_dma_buffer, 16);
        
        // Get timestamp
        sensor_data.timestamp = HAL_GetTick();
        
        // Process ADC readings with calibration
        sensor_data.temperature = adc_to_temperature(adc_dma_buffer[0]);
        sensor_data.pressure = adc_to_pressure(adc_dma_buffer[1]);
        sensor_data.flow_rate = adc_to_flow(adc_dma_buffer[2]);
        sensor_data.voltage = adc_to_voltage(adc_dma_buffer[3]);
        sensor_data.current = adc_to_current(adc_dma_buffer[4]);
        
        // Read I2C sensors (with mutex protection)
        if(xSemaphoreTake(xI2CMutex, pdMS_TO_TICKS(5)) == pdTRUE) {
            read_i2c_sensor(&sensor_data);
            xSemaphoreGive(xI2CMutex);
        }
        
        // Apply digital filtering (moving average)
        apply_filter(&sensor_data);
        
        // Check sensor validity
        sensor_data.status = validate_sensors(&sensor_data);
        
        // Send to control task
        xQueueSend(xSensorQueue, &sensor_data, 0);
        
        // Toggle heartbeat LED
        HAL_GPIO_TogglePin(GPIOC, LED_PIN);
    }
}

/**
 * Control algorithm task - PID control loop
 */
static void vControlTask(void *pvParameters) {
    SensorData_t sensor_data;
    ControlOutput_t control_output;
    float setpoint = 50.0f;  // Target temperature
    
    for(;;) {
        // Wait for sensor data
        if(xQueueReceive(xSensorQueue, &sensor_data, pdMS_TO_TICKS(100))) {
            
            // Run PID control algorithm
            float error = setpoint - sensor_data.temperature;
            control_output.pwm_duty = pid_compute(&pid_controller, error);
            
            // Advanced control logic
            if(sensor_data.pressure > 100.0f) {
                control_output.valve_position = calculate_valve_position(
                    sensor_data.pressure,
                    sensor_data.flow_rate
                );
            }
            
            // Safety checks
            if(sensor_data.temperature > 80.0f) {
                control_output.pwm_duty = 0;
                control_output.error_code = ERROR_OVER_TEMP;
            }
            
            // Update PWM output
            __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, 
                                  (uint32_t)(control_output.pwm_duty * 10));
            
            // Update relay states
            update_relays(control_output.relay_state);
            
            // Send control output for logging
            xQueueSend(xControlQueue, &control_output, 0);
        }
    }
}

/**
 * Communication task - handles UART, CAN, and network protocols
 */
static void vCommunicationTask(void *pvParameters) {
    uint8_t rx_buffer[128];
    uint8_t tx_buffer[128];
    CAN_TxHeaderTypeDef can_tx_header;
    CAN_RxHeaderTypeDef can_rx_header;
    uint32_t can_mailbox;
    
    // Configure CAN filter
    CAN_FilterTypeDef can_filter;
    can_filter.FilterBank = 0;
    can_filter.FilterMode = CAN_FILTERMODE_IDMASK;
    can_filter.FilterScale = CAN_FILTERSCALE_32BIT;
    can_filter.FilterIdHigh = 0x0000;
    can_filter.FilterIdLow = 0x0000;
    can_filter.FilterMaskIdHigh = 0x0000;
    can_filter.FilterMaskIdLow = 0x0000;
    can_filter.FilterFIFOAssignment = CAN_RX_FIFO0;
    can_filter.FilterActivation = ENABLE;
    HAL_CAN_ConfigFilter(&hcan1, &can_filter);
    
    // Start CAN
    HAL_CAN_Start(&hcan1);
    HAL_CAN_ActivateNotification(&hcan1, CAN_IT_RX_FIFO0_MSG_PENDING);
    
    for(;;) {
        // Handle UART communication
        if(HAL_UART_Receive(&huart1, rx_buffer, 128, 10) == HAL_OK) {
            process_uart_command(rx_buffer, tx_buffer);
            HAL_UART_Transmit_DMA(&huart1, tx_buffer, strlen((char*)tx_buffer));
        }
        
        // Send periodic CAN messages
        if(xSemaphoreTake(xCANMutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            can_tx_header.StdId = 0x321;
            can_tx_header.ExtId = 0x01;
            can_tx_header.RTR = CAN_RTR_DATA;
            can_tx_header.IDE = CAN_ID_STD;
            can_tx_header.DLC = 8;
            
            // Pack sensor data into CAN frame
            SensorData_t sensor_data;
            if(xQueuePeek(xSensorQueue, &sensor_data, 0)) {
                pack_can_data(tx_buffer, &sensor_data);
                HAL_CAN_AddTxMessage(&hcan1, &can_tx_header, tx_buffer, &can_mailbox);
            }
            
            xSemaphoreGive(xCANMutex);
        }
        
        // Handle Modbus RTU protocol
        handle_modbus_rtu();
        
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

/**
 * Safety monitoring task - critical safety functions
 */
static void vSafetyTask(void *pvParameters) {
    uint32_t emergency_stop = 0;
    uint32_t fault_flags = 0;
    
    for(;;) {
        // Check emergency stop button
        if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_0) == GPIO_PIN_RESET) {
            emergency_stop = 1;
            emergency_shutdown();
        }
        
        // Monitor critical parameters
        SensorData_t sensor_data;
        if(xQueuePeek(xSensorQueue, &sensor_data, 0)) {
            // Temperature limits
            if(sensor_data.temperature > 100.0f || sensor_data.temperature < -20.0f) {
                fault_flags |= FAULT_TEMP_RANGE;
            }
            
            // Pressure limits
            if(sensor_data.pressure > 150.0f) {
                fault_flags |= FAULT_OVERPRESSURE;
                activate_pressure_relief();
            }
            
            // Current limits
            if(sensor_data.current > 10.0f) {
                fault_flags |= FAULT_OVERCURRENT;
                disable_outputs();
            }
        }
        
        // Watchdog feed
        HAL_IWDG_Refresh(&hiwdg);
        
        // Update safety status LEDs
        update_safety_leds(fault_flags);
        
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

/**
 * PID control computation
 */
float pid_compute(PIDController_t *pid, float error) {
    uint32_t now = HAL_GetTick();
    float dt = (now - pid->last_time) / 1000.0f;
    
    if(dt <= 0.0f) dt = 0.01f;
    
    // Proportional term
    float p_term = pid->kp * error;
    
    // Integral term with anti-windup
    pid->integral += error * dt;
    if(pid->integral > 100.0f) pid->integral = 100.0f;
    if(pid->integral < -100.0f) pid->integral = -100.0f;
    float i_term = pid->ki * pid->integral;
    
    // Derivative term with filter
    float derivative = (error - pid->prev_error) / dt;
    float d_term = pid->kd * derivative;
    
    // Calculate output
    float output = p_term + i_term + d_term;
    
    // Clamp output
    if(output > pid->output_max) output = pid->output_max;
    if(output < pid->output_min) output = pid->output_min;
    
    // Update state
    pid->prev_error = error;
    pid->last_time = now;
    
    return output;
}

/**
 * DMA transfer complete callback
 */
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    // ADC conversion complete, data in adc_dma_buffer
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    
    // Notify sensor task
    vTaskNotifyGiveFromISR(xSensorTaskHandle, &xHigherPriorityTaskWoken);
    
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

/**
 * CAN receive callback
 */
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan) {
    CAN_RxHeaderTypeDef rx_header;
    uint8_t rx_data[8];
    
    if(HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &rx_header, rx_data) == HAL_OK) {
        // Process CAN message based on ID
        switch(rx_header.StdId) {
            case 0x100:  // Configuration update
                update_configuration(rx_data);
                break;
            case 0x200:  // Control command
                process_control_command(rx_data);
                break;
            case 0x300:  // Diagnostic request
                send_diagnostic_response();
                break;
        }
    }
}

/**
 * Hard fault handler with debugging info
 */
void HardFault_Handler(void) {
    // Get stack pointer
    __asm volatile (
        "tst lr, #4 \n"
        "ite eq \n"
        "mrseq r0, msp \n"
        "mrsne r0, psp \n"
        "b hard_fault_handler_c \n"
    );
}

void hard_fault_handler_c(uint32_t *hardfault_args) {
    volatile uint32_t r0 = hardfault_args[0];
    volatile uint32_t r1 = hardfault_args[1];
    volatile uint32_t r2 = hardfault_args[2];
    volatile uint32_t r3 = hardfault_args[3];
    volatile uint32_t r12 = hardfault_args[4];
    volatile uint32_t lr = hardfault_args[5];
    volatile uint32_t pc = hardfault_args[6];
    volatile uint32_t psr = hardfault_args[7];
    
    // Log fault information
    log_fault_info(pc, lr, psr);
    
    // Reset system
    NVIC_SystemReset();
}
```
