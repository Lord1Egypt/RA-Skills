# Auto-Close Mechanism

Automatically close idle cloud phones to save costs and resources.

---

## Overview

GeeLark cloud phones are billed by usage time. Forgotten devices can rack up unexpected charges. The auto-close mechanism automatically stops devices that have been idle for a specified timeout.

---

## Why Auto-Close?

- 💰 **Save Costs** - Billing continues while phones are running
- 🧹 **Release Resources** - Free up proxies and system resources
- 🔒 **Security Management** - Prevent accidental costs from forgetting to close

---

## Basic Usage

### 1. Create PhoneManager

```python
from scripts.phone_manager import PhoneManager

# Create manager with 5-minute timeout
manager = PhoneManager(timeout_minutes=5)
```

### 2. Start Background Monitoring

```python
# Start background monitoring thread
manager.start_monitor()

print("🔍 Background monitoring started (timeout: 5 minutes)")
```

### 3. Connect and Operate

```python
# Connect to device (phone_id is required, name is optional for display)
d = manager.connect_device("phone_id_123", ip, port, pwd, name="Android15")

# Perform operations
d(text="Settings").click()

# Activity is automatically recorded
```

### 4. Auto-Close

After 5 minutes of no activity, the device will automatically stop:

```
⚠️  Android15: Idle for 5 minutes
🛑 Stopped Android15 (phone_id)
```

---

## Complete Example

```python
import uiautomator2 as u2
from scripts.phone_manager import PhoneManager

# Create manager with 5-minute timeout
manager = PhoneManager(timeout_minutes=5)

# Start background monitoring
manager.start_monitor()

# Connect to device
adb_info = {"ip": "1.2.3.4", "port": "5555", "pwd": "password"}
d = manager.connect_device("phone_id_123",
                           adb_info['ip'],
                           adb_info['port'],
                           adb_info['pwd'],
                           name="Android15")

# Perform operations
d(text="Settings").click()

# Continue working...

# Device will auto-close after 5 minutes of no activity
```

---

## Manual Activity Recording

### Record Activity Manually

```python
# Record activity to prevent auto-close (use phone_id)
manager.record_activity("phone_id_123")
```

### Use During Long-Running Tasks

```python
def long_running_task():
    for i in range(10):
        # Do work
        process_data()

        # Record activity every 2 minutes (use phone_id)
        manager.record_activity("phone_id_123")
        time.sleep(120)

long_running_task()
```

---

## Whitelist Devices

### Add Device to Whitelist

Whitelisted devices are never auto-closed. All operations use `phone_id` for precise matching.

```python
# Add device to whitelist (use phone_id)
manager.add_to_whitelist("phone_id_123")

# Output: 📋 Android15 (phone_id_123): Added to whitelist
```

### Use for Long-Running Tasks

```python
# Add monitoring device to whitelist
manager.add_to_whitelist("monitoring_phone_id")

# This device will never be auto-closed
# Even if idle for hours
```

### Remove from Whitelist

```python
# Remove device from whitelist (use phone_id)
manager.remove_from_whitelist("phone_id_123")

print("📋 phone_id_123: Removed from whitelist")
```

---

## Configuration Options

### Timeout Configuration

```python
# 2-minute timeout (short tasks)
manager = PhoneManager(timeout_minutes=2)

# 5-minute timeout (default)
manager = PhoneManager(timeout_minutes=5)

# 10-minute timeout (long tasks)
manager = PhoneManager(timeout_minutes=10)

# 15-minute timeout (very long tasks)
manager = PhoneManager(timeout_minutes=15)
```

### Check Interval Configuration

```python
# Check every 30 seconds (default: 60)
manager.start_monitor(check_interval=30)

# Check every 60 seconds (default)
manager.start_monitor(check_interval=60)

# Check every 120 seconds (less frequent)
manager.start_monitor(check_interval=120)
```

---

## Stop All Devices

### Manual Stop All

```python
# Stop all active devices
manager.stop_all()

print("🛑 All active devices stopped")
```

### Auto-Close on Exit

Using context manager:

```python
# Automatically stop all devices on exit
with PhoneManager(timeout_minutes=5) as manager:
    manager.start_monitor()

    # Connect and operate
    d = manager.connect_device("Android15", ip, port, pwd, phone_id)
    # ...

# Automatically stops all devices when exiting context
```

---

## Best Practices

### 1. Set Appropriate Timeout

```python
# Short tasks (1-2 minutes): 2-minute timeout
manager = PhoneManager(timeout_minutes=2)

# Regular tasks: 5-minute timeout (default)
manager = PhoneManager(timeout_minutes=5)

# Long tasks: 10-15 minute timeout
manager = PhoneManager(timeout_minutes=10)
```

### 2. Record Activity During Long Tasks

```python
def long_task():
    for i in range(100):
        # Do work
        process_item(i)

        # Record activity every 2 minutes (use phone_id)
        if i % 20 == 0:  # Every 20 iterations
            manager.record_activity("phone_id_123")

long_task()
```

### 3. Use Whitelist for Critical Devices

```python
# Add monitoring device to whitelist (use phone_id)
manager.add_to_whitelist("monitoring_phone_id")

# This device will never be auto-closed
```

### 4. Use Context Manager for Cleanup

```python
# Guaranteed cleanup on exit
with PhoneManager(timeout_minutes=5) as manager:
    manager.start_monitor()

    # Connect using phone_id
    d = manager.connect_device("phone_id_123", ip, port, pwd, name="Android15")
    # ...

# Automatically stops all devices
```

### 5. Monitor Background Thread

```python
# Check if monitor thread is running
if manager.monitor_thread and manager.monitor_thread.is_alive():
    print("✅ Monitor thread is running")
else:
    print("⚠️  Monitor thread is not running")
```

---

## Advanced Usage

### Custom Idle Detection

```python
def custom_idle_check():
    """Custom idle detection logic"""
    now = datetime.now()

    for phone_id, last_time in manager.last_activity.items():
        if phone_id in manager.whitelist:
            continue  # Skip whitelisted

        idle_time = now - last_time

        # Custom logic: different timeouts for different devices
        if "Android15" in manager._display_names.get(phone_id, ""):
            timeout = timedelta(minutes=10)  # 10 minutes for Android15
        else:
            timeout = manager.timeout

        if idle_time > timeout:
            display_name = manager._display_names.get(phone_id, phone_id)
            print(f"⚠️  {display_name}: Idle for {idle_time.seconds // 60} minutes")
            manager.stop_phone(phone_id)
```

### Monitor Specific Devices

```python
# Only monitor specific devices (use phone_id)
target_devices = ["phone_id_123", "phone_id_456"]

for phone_id in list(manager.last_activity.keys()):
    if phone_id not in target_devices:
        # Skip non-target devices
        continue

    idle_time = now - manager.last_activity[phone_id]
    if idle_time > manager.timeout:
        manager.stop_phone(phone_id)
```

---

## Common Scenarios

### Scenario 1: Batch Processing

```python
manager = PhoneManager(timeout_minutes=5)
manager.start_monitor()

# Process 10 devices in batch
for i in range(10):
    phone_id = f"phone_id_{i}"
    device_name = f"Android{i}"

    # Connect and process (use phone_id)
    d = manager.connect_device(phone_id, ip, port, pwd, name=device_name)
    process_data(d)

    # Move to next device
    # Previous devices will auto-close after 5 minutes
```

### Scenario 2: Long-Running Monitoring

```python
manager = PhoneManager(timeout_minutes=10)
manager.start_monitor()

# Add monitoring device to whitelist (use phone_id)
manager.add_to_whitelist("monitoring_phone_id")

# Monitor continuously
while True:
    check_all_devices()
    manager.record_activity("monitoring_phone_id")
    time.sleep(60)
```

### Scenario 3: Interactive Testing

```python
manager = PhoneManager(timeout_minutes=2)
manager.start_monitor()

# Interactive testing loop
while True:
    command = input("Enter command (or 'quit'): ")

    if command == "quit":
        break

    # Execute command
    execute_command(command)

    # Record activity to prevent auto-close (use phone_id)
    manager.record_activity("phone_id_123")
```

---

## Troubleshooting

### Device Not Auto-Closing

**Problem**: Device should auto-close but doesn't.

**Solutions**:
1. Check if device is whitelisted
2. Check if activity is being recorded
3. Check monitor thread is running

```python
# Check whitelist
print(f"Whitelist: {manager.whitelist}")

# Check activity
print(f"Last activity: {manager.last_activity}")

# Check monitor thread
if manager.monitor_thread and manager.monitor_thread.is_alive():
    print("✅ Monitor thread is running")
else:
    print("❌ Monitor thread is not running")
```

### Device Closing Too Early

**Problem**: Device closes before expected.

**Solutions**:
1. Increase timeout
2. Record activity more frequently

```python
# Increase timeout
manager = PhoneManager(timeout_minutes=10)

# Record activity more frequently (use phone_id)
for i in range(100):
    process_item(i)
    if i % 5 == 0:  # Every 5 iterations
        manager.record_activity("phone_id_123")
```

### Monitor Thread Not Starting

**Problem**: Background monitor doesn't start.

**Solution**:
```python
# Check if start_monitor() was called
manager.start_monitor()

# Verify thread is running
if manager.monitor_thread and manager.monitor_thread.is_alive():
    print("✅ Monitor thread is running")
else:
    print("❌ Monitor thread failed to start")
```

---

## API Reference

### PhoneManager Class

```python
class PhoneManager:
    def __init__(self, timeout_minutes: int = 5, token: str = None, base_url: str = None, task_name: str = "phone_manager"):
        """
        Initialize PhoneManager.

        Args:
            timeout_minutes: Timeout in minutes before auto-closing
            token: GeeLark API token (optional, reads from config if not provided)
            base_url: API base URL (optional)
            task_name: Name for logging context
        """

    def connect_device(self, phone_id: str, ip: str, port: str, pwd: str, name: str = None) -> u2.Device:
        """
        Connect to cloud phone and record activity.

        Args:
            phone_id: Cloud phone ID (required, used for all operations)
            ip: ADB IP address
            port: ADB port
            pwd: ADB password
            name: Display name (optional, for logging only)

        Returns:
            uiautomator2.Device instance
        """

    def record_activity(self, phone_id: str):
        """
        Record cloud phone activity time.

        Args:
            phone_id: Cloud phone ID
        """

    def stop_phone(self, phone_id: str) -> bool:
        """
        Stop cloud phone.

        Args:
            phone_id: Cloud phone ID

        Returns:
            True if stopped successfully, False otherwise
        """

    def add_to_whitelist(self, phone_id: str):
        """
        Add device to whitelist (not auto-closed).

        Args:
            phone_id: Cloud phone ID
        """

    def remove_from_whitelist(self, phone_id: str):
        """
        Remove device from whitelist.

        Args:
            phone_id: Cloud phone ID
        """

    def start_monitor(self, check_interval: int = 60):
        """
        Start background monitoring thread.

        Args:
            check_interval: Check interval in seconds (default: 60)
        """

    def stop_monitor(self):
        """
        Stop background monitoring thread.
        """

    def stop_all(self):
        """
        Stop all active cloud phones and save logs.
        """
```

---

## Last Updated

2026-04-25

**Related Documents**:
- [Best Practices](best_practices.md) - Safety and performance tips
- [Phone Manager Script](../scripts/phone_manager.py) - Complete implementation