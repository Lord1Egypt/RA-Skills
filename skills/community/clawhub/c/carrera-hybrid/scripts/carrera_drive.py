#!/usr/bin/env python3
"""
Carrera HYBRID RC Car Controller
Protocol: 20-byte packets via Nordic UART BLE
"""
import asyncio
import sys
from bleak import BleakClient

ADDRESS = "YOUR_CAR_ADDRESS"
UART_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

# Base packet (idle)
BASE = bytearray([0xBF, 0x0F, 0x00, 0x08, 0x28, 0x00, 0xDF, 0x00,
                   0x86, 0x00, 0x72, 0x00, 0x02, 0xFF, 0x82, 0x00,
                   0x00, 0x00, 0x00, 0x00])

def crc8(data):
    """CRC-8 with poly=0x31, init=0xFF"""
    crc = 0xFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x31) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

def make_packet(gas=0, steer=0, light=True):
    """
    gas: -50 to +50 (negative=reverse, positive=forward)
    steer: -127 to +127 (negative=left, positive=right)
    light: True=on, False=off
    """
    pkt = bytearray(BASE)
    
    # Gas: idle=0xDF, forward=0xDF+gas (wraps around 0xFF→0x00)
    gas_byte = (0xDF + gas) & 0xFF
    pkt[6] = gas_byte
    
    # Steering: 0x00=center, 0x01-0x7F=right, 0x81-0xFF=left
    if steer >= 0:
        pkt[7] = min(steer, 0x7F)
    else:
        pkt[7] = (256 + steer) & 0xFF  # e.g. -127 → 0x81
    
    # Light: byte 14, bit 1 (0x82=on, 0x80=off)
    pkt[14] = 0x82 if light else 0x80
    
    # Checksum
    pkt[19] = crc8(pkt[:19])
    return pkt

async def drive_command(client, gas, steer, duration_ms=3000, interval_ms=50, light=True):
    """Send drive command for duration"""
    pkt = make_packet(gas, steer, light)
    count = duration_ms // interval_ms
    for _ in range(count):
        await client.write_gatt_char(UART_TX, bytes(pkt), response=False)
        await asyncio.sleep(interval_ms / 1000)

async def stop(client, duration_ms=500):
    """Send idle packets"""
    await drive_command(client, 0, 0, duration_ms)

async def main():
    if len(sys.argv) < 2:
        print("Usage: carrera_drive.py <command>")
        print("Commands: forward, back, left, right, spin, demo, idle")
        return
    
    cmd = sys.argv[1].lower()
    gas_val = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    dur = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    
    print(f"Connecting to car...")
    async with BleakClient(ADDRESS, timeout=15) as client:
        print(f"Connected! Command: {cmd}")
        
        if cmd == "forward":
            await drive_command(client, gas_val, 0, dur)
        elif cmd == "back":
            await drive_command(client, -gas_val, 0, dur)
        elif cmd == "left":
            await drive_command(client, gas_val, -100, dur)
        elif cmd == "right":
            await drive_command(client, gas_val, 100, dur)
        elif cmd == "spin":
            await drive_command(client, gas_val, -127, dur)
        elif cmd == "light_on":
            await drive_command(client, 0, 0, dur, light=True)
        elif cmd == "light_off":
            await drive_command(client, 0, 0, dur, light=False)
        elif cmd == "idle":
            await stop(client, dur)
        elif cmd == "demo":
            print("Forward...")
            await drive_command(client, 40, 0, 2000)
            await stop(client, 500)
            print("Left...")
            await drive_command(client, 40, -100, 2000)
            await stop(client, 500)
            print("Right...")
            await drive_command(client, 40, 100, 2000)
            await stop(client, 500)
            print("Back...")
            await drive_command(client, -40, 0, 2000)
            await stop(client, 500)
        else:
            print(f"Unknown command: {cmd}")
            return
        
        # Always end with idle
        await stop(client, 300)
        print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
