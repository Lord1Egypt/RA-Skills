"""Tests for device module - Multi-device support."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from clawshorts.device import Device
from clawshorts import config


class TestDevice(unittest.TestCase):
    """Test Device model."""

    def test_device_creation_with_all_fields(self):
        """Test creating device with all fields."""
        device = Device(ip="192.168.1.100", name="living-room", limit=10, enabled=True)
        self.assertEqual(device.ip, "192.168.1.100")
        self.assertEqual(device.name, "living-room")
        self.assertEqual(device.limit, 10)
        self.assertTrue(device.enabled)

    def test_device_creation_minimal(self):
        """Test creating device with minimal fields — name auto-generated."""
        device = Device(ip="192.168.1.100")
        self.assertEqual(device.ip, "192.168.1.100")
        self.assertEqual(device.name, "tv-192-168-1-100")
        self.assertEqual(device.limit, 5)
        self.assertTrue(device.enabled)

    def test_device_invalid_ip_format(self):
        """Test invalid IP format is rejected."""
        with self.assertRaises(ValueError) as ctx:
            Device(ip="invalid-ip")
        self.assertIn("Invalid IP", str(ctx.exception))

    def test_device_invalid_ip_octet(self):
        """Test IP with octet > 255 is rejected."""
        with self.assertRaises(ValueError) as ctx:
            Device(ip="192.168.1.300")
        self.assertIn("Invalid IP", str(ctx.exception))

    def test_device_name_sanitization(self):
        """Test name is sanitized — special characters removed."""
        device = Device(ip="192.168.1.100", name="living room@#!")
        self.assertEqual(device.name, "livingroom")

    def test_device_name_auto_generated(self):
        """Test auto-generated name from IP."""
        device = Device(ip="10.0.0.50")
        self.assertEqual(device.name, "tv-10-0-0-50")

    def test_device_model_dump(self):
        """Test serialization to dictionary via Pydantic v2 model_dump."""
        device = Device(ip="192.168.1.100", name="test", limit=3, enabled=False)
        d = device.model_dump()
        self.assertEqual(d["ip"], "192.168.1.100")
        self.assertEqual(d["name"], "test")
        self.assertEqual(d["limit"], 3)
        self.assertFalse(d["enabled"])

    def test_device_model_validate(self):
        """Test deserialization from dictionary via Pydantic v2 model_validate."""
        data = {"ip": "192.168.1.100", "name": "test", "limit": 3, "enabled": True}
        device = Device.model_validate(data)
        self.assertEqual(device.ip, "192.168.1.100")
        self.assertEqual(device.name, "test")
        self.assertEqual(device.limit, 3)
        self.assertTrue(device.enabled)


class TestConfigValidation(unittest.TestCase):
    """Test config validation functions."""

    def test_validate_valid_ip(self):
        """Test validation of valid IP."""
        valid, error = config.validate_device_input("192.168.1.100")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_validate_valid_ip_with_name(self):
        """Test validation of valid IP with name."""
        valid, error = config.validate_device_input("192.168.1.100", "living-room")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_validate_invalid_ip_format(self):
        """Test invalid IP format."""
        valid, error = config.validate_device_input("not-an-ip")
        self.assertFalse(valid)
        self.assertIn("Invalid IP", error)

    def test_validate_invalid_ip_octet(self):
        """Test IP with invalid octet."""
        valid, error = config.validate_device_input("192.168.1.300")
        self.assertFalse(valid)
        self.assertIn("Invalid IP", error)

    def test_validate_invalid_name_special_chars(self):
        """Test name with special characters."""
        valid, error = config.validate_device_input("192.168.1.100", "test@#$%")
        self.assertFalse(valid)
        self.assertIn("alphanumeric", error)

    def test_validate_invalid_name_too_long(self):
        """Test name too long."""
        valid, error = config.validate_device_input("192.168.1.100", "a" * 60)
        self.assertFalse(valid)
        self.assertIn("50 characters", error)


class TestConfigPersistence(unittest.TestCase):
    """Test config file operations."""

    def setUp(self):
        """Set up temp config."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "devices.yaml"
        config.set_config_path(self.config_path)

    def tearDown(self):
        """Clean up temp config."""
        config.set_config_path(Path.home() / ".clawshorts" / "devices.yaml")
        self.temp_dir.cleanup()

    def test_add_device(self):
        """Test adding a device."""
        device = config.add_device("192.168.1.100", "living-room", 5)
        self.assertEqual(device.ip, "192.168.1.100")
        self.assertEqual(device.name, "living-room")

    def test_add_device_auto_name(self):
        """Test adding device with auto-generated name."""
        device = config.add_device("192.168.1.100")
        self.assertEqual(device.name, "tv-192-168-1-100")

    def test_add_duplicate_device(self):
        """Test adding duplicate device raises error."""
        config.add_device("192.168.1.100", "test")
        with self.assertRaises(config.ConfigError) as ctx:
            config.add_device("192.168.1.100", "test2")
        self.assertIn("already exists", str(ctx.exception))

    def test_remove_device(self):
        """Test removing a device."""
        config.add_device("192.168.1.100")
        removed = config.remove_device("192.168.1.100")
        self.assertTrue(removed)

    def test_remove_nonexistent_device(self):
        """Test removing nonexistent device returns False."""
        removed = config.remove_device("192.168.1.999")
        self.assertFalse(removed)

    def test_load_devices(self):
        """Test loading devices."""
        config.add_device("192.168.1.100", "living-room")
        config.add_device("192.168.1.101", "bedroom", 3)
        devices = config.load_devices()
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0].name, "living-room")
        self.assertEqual(devices[1].name, "bedroom")

    def test_get_device(self):
        """Test getting a specific device."""
        config.add_device("192.168.1.100", "living-room")
        device = config.get_device("192.168.1.100")
        self.assertIsNotNone(device)
        self.assertEqual(device.name, "living-room")

    def test_get_nonexistent_device(self):
        """Test getting nonexistent device returns None."""
        device = config.get_device("192.168.1.999")
        self.assertIsNone(device)

    def test_update_device(self):
        """Test updating device fields."""
        config.add_device("192.168.1.100", "original")
        updated = config.update_device("192.168.1.100", name="updated", limit=10)
        self.assertEqual(updated.name, "updated")
        self.assertEqual(updated.limit, 10)

    def test_persistence(self):
        """Test config persists after reload."""
        config.add_device("192.168.1.100", "test")
        devices = config.load_devices()
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].ip, "192.168.1.100")


if __name__ == "__main__":
    unittest.main()
