#!/usr/bin/env python3
"""
Import driver card tachograph data from JSON to SQLite.
"""
import json
import sqlite3
import sys
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'tachograph.db')


def load_json(filepath: str) -> dict:
    """Load JSON from file, handling parser warnings."""
    with open(filepath, 'r') as f:
        content = f.read()
    # Skip warnings in output (first lines starting with date)
    json_start = content.find('{')
    if json_start < 0:
        raise ValueError("No JSON found in file")
    return json.loads(content[json_start:])


def init_db(conn: sqlite3.Connection):
    """Initialize database schema."""
    cursor = conn.cursor()
    
    # Driver card identification
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS driver_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT UNIQUE,
            issuing_member_state INTEGER,
            issuing_authority TEXT,
            issue_date TEXT,
            validity_begin TEXT,
            expiry_date TEXT,
            driver_surname TEXT,
            driver_first_names TEXT,
            birth_date TEXT,
            preferred_language TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Daily activity records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            record_date TEXT,
            presence_counter INTEGER,
            day_distance INTEGER,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Activity changes (work periods)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_activity_id INTEGER,
            record_date TEXT,
            minutes INTEGER,
            work_type INTEGER,
            card_present INTEGER,
            is_driver INTEGER,
            is_team INTEGER,
            FOREIGN KEY (daily_activity_id) REFERENCES daily_activities(id)
        )
    ''')
    
    # Vehicles used
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles_used (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            vehicle_registration_nation INTEGER,
            vehicle_registration_number TEXT,
            vu_approval_number TEXT,
            vu_serial_number TEXT,
            first_use TEXT,
            last_use TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Events
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS card_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            event_type INTEGER,
            event_begin_time TEXT,
            event_end_time TEXT,
            vehicle_nation INTEGER,
            vehicle_number TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Faults
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS card_faults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            fault_type INTEGER,
            fault_begin_time TEXT,
            fault_end_time TEXT,
            vehicle_nation INTEGER,
            vehicle_number TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Work periods (place records)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_periods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            entry_time TEXT,
            entry_type_daily_work_period INTEGER,
            daily_work_period_country INTEGER,
            daily_work_period_region INTEGER,
            vehicle_odometer_value INTEGER,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Border crossings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS border_crossings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            country_left INTEGER,
            country_entered INTEGER,
            gnss_place_record TEXT,
            vehicle_odometer_value INTEGER,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Load/Unload operations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS load_unload (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            timestamp TEXT,
            operation_type INTEGER,
            gnss_place_record TEXT,
            vehicle_odometer_value INTEGER,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Control activity records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            control_type INTEGER,
            control_time TEXT,
            control_card_number TEXT,
            control_vehicle_nation INTEGER,
            control_vehicle_number TEXT,
            control_download_period_begin TEXT,
            control_download_period_end TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Current session (card current use)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            session_open_time TEXT,
            session_vehicle_nation INTEGER,
            session_vehicle_number TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # Last card download
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS last_download (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            last_download_time TEXT,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    # GNSS locations (accumulated driving)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gnss_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT,
            time_stamp TEXT,
            gnss_place_record TEXT,
            vehicle_odometer_value INTEGER,
            imported_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_number) REFERENCES driver_cards(card_number)
        )
    ''')
    
    conn.commit()


def import_driver_card(conn: sqlite3.Connection, data: dict):
    """Import driver card identification."""
    driver_id = data.get('card_identification_and_driver_card_holder_identification_1', {})
    if not driver_id:
        print("No driver identification found")
        return None
    
    card_id = driver_id.get('card_identification', {})
    holder = driver_id.get('driver_card_holder_identification', {})
    
    card_number = card_id.get('card_number')
    if not card_number:
        print("No card number found")
        return None
    
    # Parse birth date
    birth = holder.get('card_holder_birth_date', {})
    birth_date = None
    if birth:
        birth_date = f"{birth.get('year', '')}-{birth.get('month', ''):02d}-{birth.get('day', ''):02d}"
    
    name = holder.get('card_holder_name', {})
    surname = name.get('holder_surname', '')
    first_names = name.get('holder_first_names', '')
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO driver_cards (
            card_number, issuing_member_state, issuing_authority,
            issue_date, validity_begin, expiry_date,
            driver_surname, driver_first_names, birth_date, preferred_language
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        card_number,
        card_id.get('card_issuing_member_state'),
        card_id.get('card_issuing_authority_name'),
        card_id.get('card_issue_date'),
        card_id.get('card_validity_begin'),
        card_id.get('card_expiry_date'),
        surname,
        first_names,
        birth_date,
        holder.get('card_holder_preferred_language')
    ))
    conn.commit()
    print(f"Imported driver card: {card_number}")
    return card_number


def import_activities(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import daily activity records."""
    activity = data.get('card_driver_activity_1', {})
    decoded_records = activity.get('decoded_activity_daily_records', [])
    
    cursor = conn.cursor()
    activity_ids = []
    
    for record in decoded_records:
        record_date = record.get('activity_record_date')
        if not record_date:
            continue
        
        cursor.execute('''
            INSERT INTO daily_activities (card_number, record_date, presence_counter, day_distance)
            VALUES (?, ?, ?, ?)
        ''', (
            card_number,
            record_date,
            record.get('activity_daily_presence_counter'),
            record.get('activity_day_distance')
        ))
        activity_id = cursor.lastrowid
        activity_ids.append(activity_id)
        
        # Import activity changes
        for change in record.get('activity_change_info', []):
            cursor.execute('''
                INSERT INTO activity_changes (
                    daily_activity_id, record_date, minutes, work_type,
                    card_present, is_driver, is_team
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                activity_id,
                record_date,
                change.get('minutes'),
                change.get('work_type'),
                int(change.get('card_present', False)),
                int(change.get('driver', False)),
                int(change.get('team', False))
            ))
    
    conn.commit()
    print(f"Imported {len(activity_ids)} daily activity records")


def import_vehicles(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import vehicles used."""
    vehicles = data.get('card_vehicles_used_1', {})
    vehicle_records = vehicles.get('card_vehicle_records', [])
    
    cursor = conn.cursor()
    for v in vehicle_records:
        vu = v.get('vehicle_registration', {})
        cursor.execute('''
            INSERT INTO vehicles_used (
                card_number, vehicle_registration_nation, vehicle_registration_number,
                vu_approval_number, vu_serial_number, first_use, last_use
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            card_number,
            vu.get('vehicle_registration_nation'),
            vu.get('vehicle_registration_number'),
            v.get('vu_approval_number'),
            v.get('vu_serial_number'),
            v.get('first_use'),
            v.get('last_use')
        ))
    
    conn.commit()
    print(f"Imported {len(vehicle_records)} vehicle records")


def import_events(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import events."""
    events = data.get('card_event_data_1', {})
    event_records = events.get('card_event_records_array', [])
    
    cursor = conn.cursor()
    count = 0
    for day in event_records:
        for event in day.get('card_event_records', []):
            if event.get('event_type', 0) == 0:
                continue  # Skip empty
            cursor.execute('''
                INSERT INTO card_events (
                    card_number, event_type, event_begin_time, event_end_time,
                    vehicle_nation, vehicle_number
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                card_number,
                event.get('event_type'),
                event.get('event_begin_time'),
                event.get('event_end_time'),
                event.get('event_vehicle_registration', {}).get('vehicle_registration_nation'),
                event.get('event_vehicle_registration', {}).get('vehicle_registration_number')
            ))
            count += 1
    
    conn.commit()
    print(f"Imported {count} events")


def import_faults(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import faults."""
    faults = data.get('card_fault_data_1', {})
    fault_records = faults.get('card_fault_records_array', [])
    
    cursor = conn.cursor()
    count = 0
    for day in fault_records:
        for fault in day.get('card_fault_records', []):
            if fault.get('fault_type', 0) == 0:
                continue  # Skip empty
            cursor.execute('''
                INSERT INTO card_faults (
                    card_number, fault_type, fault_begin_time, fault_end_time,
                    vehicle_nation, vehicle_number
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                card_number,
                fault.get('fault_type'),
                fault.get('fault_begin_time'),
                fault.get('fault_end_time'),
                fault.get('fault_vehicle_registration', {}).get('vehicle_registration_nation'),
                fault.get('fault_vehicle_registration', {}).get('vehicle_registration_number')
            ))
            count += 1
    
    conn.commit()
    print(f"Imported {count} faults")


def import_work_periods(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import work periods (place records)."""
    wp = data.get('card_place_daily_work_period_1', {})
    records = wp.get('place_records', [])
    
    cursor = conn.cursor()
    for r in records:
        cursor.execute('''
            INSERT INTO work_periods (
                card_number, entry_time, entry_type_daily_work_period,
                daily_work_period_country, daily_work_period_region,
                vehicle_odometer_value
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            card_number,
            r.get('entry_time'),
            r.get('entry_type_daily_work_period'),
            r.get('daily_work_period_country'),
            r.get('daily_work_period_region'),
            r.get('vehicle_odometer_value')
        ))
    
    conn.commit()
    print(f"Imported {len(records)} work period records")


def import_border_crossings(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import border crossings."""
    bc = data.get('card_border_crossings', {})
    records = bc.get('card_border_crossing_records', [])
    
    cursor = conn.cursor()
    for r in records:
        gnss = r.get('gnss_place_auth_record', {})
        cursor.execute('''
            INSERT INTO border_crossings (
                card_number, country_left, country_entered,
                gnss_place_record, vehicle_odometer_value
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            card_number,
            r.get('country_left'),
            r.get('country_entered'),
            json.dumps(gnss),
            r.get('vehicle_odometer_value')
        ))
    
    conn.commit()
    print(f"Imported {len(records)} border crossing records")


def import_load_unload(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import load/unload operations."""
    lu = data.get('card_load_unload_operations', {})
    records = lu.get('card_load_unload_records', [])
    
    cursor = conn.cursor()
    for r in records:
        gnss = r.get('gnss_place_auth_record', {})
        cursor.execute('''
            INSERT INTO load_unload (
                card_number, timestamp, operation_type,
                gnss_place_record, vehicle_odometer_value
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            card_number,
            r.get('timestamp'),
            r.get('operation_type'),
            json.dumps(gnss),
            r.get('vehicle_odometer_value')
        ))
    
    conn.commit()
    print(f"Imported {len(records)} load/unload records")


def import_controls(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import control activity records."""
    ctrl = data.get('card_control_activity_data_record_1', {})
    
    cursor = conn.cursor()
    if ctrl.get('control_type'):
        vr = ctrl.get('control_vehicle_registration', {})
        cursor.execute('''
            INSERT INTO controls (
                card_number, control_type, control_time,
                control_card_number, control_vehicle_nation, control_vehicle_number,
                control_download_period_begin, control_download_period_end
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            card_number,
            ctrl.get('control_type'),
            ctrl.get('control_time'),
            ctrl.get('control_card_number'),
            vr.get('vehicle_registration_nation'),
            vr.get('vehicle_registration_number'),
            ctrl.get('control_download_period_begin'),
            ctrl.get('control_download_period_end')
        ))
    
    conn.commit()
    print(f"Imported control record")


def import_current_session(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import current session (card current use)."""
    cs = data.get('card_current_use_1', {})
    
    cursor = conn.cursor()
    if cs.get('session_open_time'):
        vr = cs.get('session_open_vehicle', {})
        cursor.execute('''
            INSERT INTO current_session (
                card_number, session_open_time,
                session_vehicle_nation, session_vehicle_number
            ) VALUES (?, ?, ?, ?)
        ''', (
            card_number,
            cs.get('session_open_time'),
            vr.get('vehicle_registration_nation'),
            vr.get('vehicle_registration_number')
        ))
    
    conn.commit()
    print(f"Imported current session")


def import_last_download(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import last card download."""
    ld = data.get('last_card_download_1', {})
    download_time = ld.get('last_card_download')
    
    cursor = conn.cursor()
    if download_time:
        cursor.execute('''
            INSERT INTO last_download (card_number, last_download_time)
            VALUES (?, ?)
        ''', (card_number, download_time))
    
    conn.commit()
    print(f"Imported last download: {download_time}")


def import_gnss_locations(conn: sqlite3.Connection, card_number: str, data: dict):
    """Import GNSS locations (accumulated driving)."""
    gnss = data.get('gnss_accumulated_driving', {})
    records = gnss.get('gnss_accumulated_driving_records', [])
    
    cursor = conn.cursor()
    for r in records:
        gnss_place = r.get('gnss_place_record', {})
        cursor.execute('''
            INSERT INTO gnss_locations (
                card_number, time_stamp, gnss_place_record, vehicle_odometer_value
            ) VALUES (?, ?, ?, ?)
        ''', (
            card_number,
            r.get('time_stamp'),
            json.dumps(gnss_place),
            r.get('vehicle_odometer_value')
        ))
    
    conn.commit()
    print(f"Imported {len(records)} GNSS location records")


def main():
    if len(sys.argv) < 2:
        print("Usage: import.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    if not os.path.exists(json_file):
        print(f"File not found: {json_file}")
        sys.exit(1)
    
    print(f"Loading {json_file}...")
    data = load_json(json_file)
    
    # Connect to DB
    db_path = os.path.abspath(DB_PATH)
    print(f"Using database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    try:
        init_db(conn)
        
        # Import data
        card_number = import_driver_card(conn, data)
        if card_number:
            import_activities(conn, card_number, data)
            import_vehicles(conn, card_number, data)
            import_events(conn, card_number, data)
            import_faults(conn, card_number, data)
            import_work_periods(conn, card_number, data)
            import_border_crossings(conn, card_number, data)
            import_load_unload(conn, card_number, data)
            import_controls(conn, card_number, data)
            import_current_session(conn, card_number, data)
            import_last_download(conn, card_number, data)
            import_gnss_locations(conn, card_number, data)
        
        print("Import complete!")
        
    finally:
        conn.close()


if __name__ == '__main__':
    main()