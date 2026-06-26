#!/usr/bin/env python3
"""
Relay Control Module
"""

import serial
import time


class Relay:
    """USB Relay Control Class"""

    def __init__(self, port='/dev/ttyUSB1', baudrate=9600, timeout=1):
        """
        Initialize Relay

        Args:
            port: Serial port, default '/dev/ttyUSB1'
            baudrate: Baud rate, default 9600
            timeout: Timeout in seconds, default 1
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.relay_state = False

    def connect(self):
        """
        Connect to Relay

        Returns:
            bool: True if connection successful
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(0.5)
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to relay: {e}")
            return False

    def disconnect(self):
        """Disconnect from Relay"""
        if self.serial and self.serial.is_open:
            self.serial.close()

    def turn_on(self):
        """
        Turn on Relay

        Command: A0 01 01 A2

        Returns:
            bool: True if operation successful
        """
        return self._send_command(bytes([0xA0, 0x01, 0x01, 0xA2]), True)

    def turn_off(self):
        """
        Turn off Relay

        Command: A0 01 00 A1

        Returns:
            bool: True if operation successful
        """
        return self._send_command(bytes([0xA0, 0x01, 0x00, 0xA1]), False)

    def toggle(self):
        """
        Toggle Relay State

        Returns:
            bool: True if operation successful
        """
        if self.relay_state:
            return self.turn_off()
        else:
            return self.turn_on()

    def _send_command(self, cmd, state):
        """
        Send Command to Relay

        Args:
            cmd: Command bytes
            state: Target state

        Returns:
            bool: True if send successful
        """
        if not self.serial or not self.serial.is_open:
            return False

        try:
            self.serial.write(cmd)
            time.sleep(0.1)

            # Read response (if any)
            if self.serial.in_waiting > 0:
                self.serial.read(self.serial.in_waiting)

            self.relay_state = state
            return True

        except Exception as e:
            print(f"Failed to send command: {e}")
            return False

    def get_status(self):
        """
        Get Relay Status

        Returns:
            bool: Current state
        """
        return self.relay_state

    def is_on(self):
        """
        Check if Relay is ON

        Returns:
            bool: True if ON
        """
        return self.relay_state

    def is_off(self):
        """
        Check if Relay is OFF

        Returns:
            bool: True if OFF
        """
        return not self.relay_state


if __name__ == "__main__":
    # Test example
    relay = Relay()

    if relay.connect():
        print("Relay connected successfully")

        print("Turning ON relay...")
        relay.turn_on()
        time.sleep(1)

        print("Turning OFF relay...")
        relay.turn_off()
        time.sleep(1)

        print("Toggling relay...")
        relay.toggle()
        time.sleep(1)

        print(f"Current state: {'ON' if relay.get_status() else 'OFF'}")

        relay.disconnect()
        print("Relay disconnected")
