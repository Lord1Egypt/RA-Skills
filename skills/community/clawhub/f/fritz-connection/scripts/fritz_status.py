#!/usr/bin/env python3
"""
FritzBox Status Checker
Lädt Credentials aus ~/.openclaw/skills/.env
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Fallback: skill-lokales .env
SKILL_ENV = Path(__file__).parent.parent / ".env"
OPENCLAW_ENV = Path.home() / ".openclaw" / "skills" / ".env"


def load_env():
    """Lädt .env aus global OpenClaw skills oder skill-lokal"""
    env_file = OPENCLAW_ENV if OPENCLAW_ENV.exists() else SKILL_ENV
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
    else:
        print(f"⚠️  Keine .env gefunden. Gesucht:", file=sys.stderr)
        print(f"   - {OPENCLAW_ENV}", file=sys.stderr)
        print(f"   - {SKILL_ENV}", file=sys.stderr)
        sys.exit(1)


def get_fc():
    """Erstellt FritzConnection-Objekt"""
    from fritzconnection import FritzConnection

    load_env()

    host = os.getenv("FRITZBOX_HOST")
    password = os.getenv("FRITZBOX_PASSWORD")

    if not host or not password:
        print("⚠️  FRITZBOX_HOST und/oder FRITZBOX_PASSWORD nicht gesetzt", file=sys.stderr)
        sys.exit(1)

    return FritzConnection(address=host, password=password)


def cmd_status(args):
    """Zeigt FritzBox-Status"""
    fc = get_fc()

    # Device info
    device_info = fc.call_action("DeviceInfo:1", "GetInfo")
    model = device_info.get("NewModelName", "Unknown")

    # WAN status
    try:
        wan_status = fc.call_action("WANIPConnection:1", "GetStatusInfo")
        connection_status = wan_status.get("NewConnectionStatus", "Unknown")
        uptime = wan_status.get("NewUptime", 0)
        last_error = wan_status.get("LastConnectionError", "None")
    except Exception:
        connection_status = "Unknown"
        uptime = 0
        last_error = "Unknown"

    # External IP
    try:
        external_ip = fc.call_action("WANIPConnection:1", "GetExternalIPAddress").get("NewExternalIPAddress", "Unknown")
    except Exception:
        external_ip = "Unknown"

    # Uptime formatieren
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60

    print(f"🖥️  AVM {model}")
    print(f"📍 Host: {os.getenv('FRITZBOX_HOST')}")
    print(f"🔌 Connection: {connection_status}")
    print(f"⏱️  Uptime: {uptime} seconds ({hours}h {minutes}m)")
    print(f"🌐 External IP: {external_ip}")
    if last_error and last_error != "ERROR_NONE":
        print(f"⚠️  Last Error: {last_error}")


def cmd_traffic(args):
    """Zeigt Traffic-Stats (falls verfügbar)"""
    fc = get_fc()

    try:
        # WAN Common Interface Config
        common_config = fc.call_action("WANCommonInterfaceConfig:1", "GetCommonLinkProperties")
        downstream = common_config.get("NewLayer1DownstreamMaxBitRate", 0) / 1_000_000
        upstream = common_config.get("NewLayer1UpstreamMaxBitRate", 0) / 1_000_000

        # AddonStats (optional)
        try:
            stats = fc.call_action("WANCommonInterfaceConfig:1", "GetTotalBytesReceived")
            bytes_received = stats.get("NewTotalBytesReceived", 0)
            stats_sent = fc.call_action("WANCommonInterfaceConfig:1", "GetTotalBytesSent")
            bytes_sent = stats_sent.get("NewTotalBytesSent", 0)

            print(f"📥 Max Downstream: {downstream:.0f} Mbit/s")
            print(f"📤 Max Upstream: {upstream:.0f} Mbit/s")
            print(f"📊 Total Received: {bytes_received / 1_000_000_000:.2f} GB")
            print(f"📊 Total Sent: {bytes_sent / 1_000_000_000:.2f} GB")
        except Exception:
            print(f"📥 Max Downstream: {downstream:.0f} Mbit/s")
            print(f"📤 Max Upstream: {upstream:.0f} Mbit/s")
            print("⚠️  Byte-Counter nicht verfügbar (nur Link-Speed)")
    except Exception as e:
        print(f"⚠️  Traffic-Info nicht verfügbar: {e}")


def cmd_hosts(args):
    """Listet verbundene Geräte"""
    fc = get_fc()

    try:
        hosts = fc.call_action("Hosts:1", "GetHostNumberOfEntries")
        count = hosts.get("NewHostNumberOfEntries", 0)
        print(f"📱 Verbundene Geräte: {count}")

        if args.verbose:
            for i in range(count):
                try:
                    host_info = fc.call_action("Hosts:1", "GetGenericHostEntry", NewIndex=i)
                    name = host_info.get("NewHostName", "Unknown")
                    ip = host_info.get("NewIPAddress", "Unknown")
                    mac = host_info.get("NewMACAddress", "Unknown")
                    active = "✅" if host_info.get("NewActive", False) else "⏸️"
                    print(f"   {active} {name} ({ip}, {mac})")
                except Exception:
                    pass
    except Exception as e:
        print(f"⚠️  Host-Liste nicht verfügbar: {e}")
        print("   Manche FritzBox-Modelle unterstützen dies nicht via UPnP.")


def cmd_reconnect(args):
    """Erzwingt Reconnect (neue IP)"""
    fc = get_fc()

    try:
        fc.call_action("WANIPConnection:1", "ForceTermination")
        print("🔄 Reconnect angefordert. Warte auf neue Verbindung...")
    except Exception as e:
        print(f"⚠️  Reconnect fehlgeschlagen: {e}")
        print("   Manche Provider erlauben dies nicht.")


def cmd_reboot(args):
    """Führt einen Router-Reboot durch"""
    fc = get_fc()

    try:
        fc.call_action("DeviceConfig:1", "Reboot")
        print("🔄 Reboot angefordert. Die FRITZ!Box startet jetzt neu.")
        print("   ⏱️  Das dauert normalerweise 2-5 Minuten.")
        print("   📡 Alle Geräte verlieren die Verbindung (Internet, WLAN, Telefonie).")
    except Exception as e:
        print(f"⚠️  Reboot fehlgeschlagen: {e}")
        print("   Manche FritzBox-Modelle unterstützen dies nicht via UPnP.")


def cmd_calls(args):
    """Zeigt Anrufliste"""
    import urllib.request
    import xml.etree.ElementTree as ET

    fc = get_fc()
    host = os.getenv("FRITZBOX_HOST")

    try:
        # CallList-URL holen
        result = fc.call_action("X_AVM-DE_OnTel:1", "GetCallList")
        call_list_url = result.get("NewCallListURL")

        if not call_list_url:
            print("⚠️  Keine CallList-URL erhalten")
            return

        # XML herunterladen
        with urllib.request.urlopen(call_list_url) as response:
            xml_data = response.read()

        # XML parsen
        root = ET.fromstring(xml_data)

        # Timestamp-Map für CallTypes
        # 1 = eingehend, 2 = verpasst, 3 = ausgehend
        call_types = {"1": "📞 Eingehend", "2": "📵 Verpasst", "3": "📱 Ausgehend"}

        calls = []
        for call in root.findall(".//Call"):
            call_type = call.find("Type")
            caller = call.find("Caller")
            called = call.find("Called")
            name = call.find("Name")
            timestamp = call.find("Date")
            duration = call.find("Duration")

            if call_type is not None and timestamp is not None:
                calls.append({
                    "type": call_types.get(call_type.text, "❓ Unbekannt"),
                    "caller": caller.text if caller is not None and caller.text else "Unbekannt",
                    "called": called.text if called is not None and called.text else "Unbekannt",
                    "name": name.text if name is not None and name.text else "",
                    "date": timestamp.text if timestamp is not None else "",
                    "duration": duration.text if duration is not None else "0:00"
                })

        if not calls:
            print("📭 Keine Anrufe in der Liste")
            return

        # Limit
        limit = args.limit if hasattr(args, "limit") else 10
        calls = calls[:limit]

        print(f"📋 Anrufliste ({len(calls)} Einträge)")
        print()

        for call in calls:
            caller_display = call["name"] if call["name"] else call["caller"]
            date_str = call["date"]
            duration_str = call["duration"]

            # Datum formatieren (DD.MM.YY HH:MM)
            try:
                dt = datetime.strptime(date_str, "%d.%m.%y %H:%M")
                date_formatted = dt.strftime("%d.%m.%Y %H:%M")
            except:
                date_formatted = date_str

            print(f"{call['type']}")
            print(f"   📞 {caller_display}")
            print(f"   🕐 {date_formatted} ({duration_str})")
            print()

        # Letzter Anruf Info
        if calls:
            last = calls[0]
            caller_display = last["name"] if last["name"] else last["caller"]
            print(f"📌 Letzter Anruf: {last['type']} von {caller_display} am {last['date']}")

    except Exception as e:
        print(f"⚠️  Anrufliste nicht verfügbar: {e}")
        print("   Manche FritzBox-Modelle unterstützen dies nicht via UPnP.")


def cmd_wlan(args):
    """Zeigt oder ändert WLAN-Status aller Netzwerke"""
    fc = get_fc()

    # WLAN-Netzwerke: 1=2.4GHz, 2=5GHz, 3=Gastzugang
    wlan_configs = [
        (1, "2.4 GHz", "📶"),
        (2, "5 GHz", "📡"),
        (3, "Gastzugang", "🏠"),
    ]

    # Wenn on/off Parameter gesetzt ist, erst ändern
    if hasattr(args, "action") and args.action in ["on", "off"]:
        enable = args.action == "on"
        action_verb = "Aktiviere" if enable else "Deaktiviere"
        status_text = "an" if enable else "aus"

        print(f"🔄 {action_verb} WLAN...")
        print()

        for idx, name, icon in wlan_configs:
            try:
                fc.call_action(f"WLANConfiguration:{idx}", "SetEnable", NewEnable=enable)
                status_icon = "✅" if enable else "❌"
                print(f"   {icon} {name}: {status_icon} {status_text}")
            except Exception as e:
                print(f"   {icon} {name}: ⚠️ Fehler: {e}")

        # Kurz warten
        time.sleep(1)
        print()

    # Status anzeigen
    print("📡 WLAN-Status")
    print()

    any_enabled = False

    for idx, name, icon in wlan_configs:
        try:
            info = fc.call_action(f"WLANConfiguration:{idx}", "GetInfo")
            enabled = info.get("NewEnable", False)
            status = info.get("NewStatus", "Unknown")
            ssid = info.get("NewSSID", "Unknown")
            channel = info.get("NewChannel", "?")
            standard = info.get("NewStandard", "?")

            status_icon = "✅" if enabled else "❌"
            any_enabled = any_enabled or enabled

            print(f"{icon} {name}:")
            print(f"   Status: {status_icon} {status}")
            print(f"   SSID: {ssid}")
            if enabled:
                print(f"   Kanal: {channel}")
                print(f"   Standard: {standard}")
            print()
        except Exception as e:
            print(f"{icon} {name}: ⚠️ Nicht verfügbar")
            print()

    # Gesamtstatus
    if any_enabled:
        print("📡 WLAN ist AN")
    else:
        print("📴 WLAN ist AUS")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="FritzBox Status Tool")
    subparsers = parser.add_subparsers(dest="command")

    # status
    p_status = subparsers.add_parser("status", help="Zeigt FritzBox-Status")
    p_status.set_defaults(func=cmd_status)

    # traffic
    p_traffic = subparsers.add_parser("traffic", help="Zeigt Traffic-Stats")
    p_traffic.set_defaults(func=cmd_traffic)

    # hosts
    p_hosts = subparsers.add_parser("hosts", help="Listet verbundene Geräte")
    p_hosts.add_argument("-v", "--verbose", action="store_true", help="Zeigt Details pro Gerät")
    p_hosts.set_defaults(func=cmd_hosts)

    # reconnect
    p_reconnect = subparsers.add_parser("reconnect", help="Erzwingt Reconnect")
    p_reconnect.set_defaults(func=cmd_reconnect)

    # reboot
    p_reboot = subparsers.add_parser("reboot", help="Startet die FRITZ!Box neu")
    p_reboot.set_defaults(func=cmd_reboot)

    # calls
    p_calls = subparsers.add_parser("calls", help="Zeigt Anrufliste")
    p_calls.add_argument("-n", "--limit", type=int, default=10, help="Anzahl Einträge (default: 10)")
    p_calls.set_defaults(func=cmd_calls)

    # wlan
    p_wlan = subparsers.add_parser("wlan", help="Zeigt oder ändert WLAN-Status")
    p_wlan.add_argument("action", nargs="?", choices=["on", "off"], help="WLAN an/aus schalten")
    p_wlan.set_defaults(func=cmd_wlan)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()