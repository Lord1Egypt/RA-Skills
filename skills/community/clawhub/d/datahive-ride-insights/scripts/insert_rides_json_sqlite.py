#!/usr/bin/env python3
"""Insert extracted ride-insights records from rides.json into SQLite."""

import argparse
import json
import sqlite3
from pathlib import Path

FIELDS = [
    'provider', 'gmail_message_id', 'email_date_text', 'subject',
    'start_time_text', 'end_time_text', 'total_text', 'currency', 'amount',
    'pickup', 'dropoff', 'pickup_city', 'pickup_country', 'dropoff_city', 'dropoff_country',
    'payment_method', 'driver', 'distance_text', 'duration_text', 'notes',
    'extracted_ride_json'
]


def main():
    ap = argparse.ArgumentParser(description='Insert extracted ride-insights records into SQLite')
    ap.add_argument('--db', required=True, help='Path to the ride-insights SQLite database')
    ap.add_argument('--rides-json', required=True, help='Path to the extracted rides.json file')
    args = ap.parse_args()

    rides = json.loads(Path(args.rides_json).read_text(encoding='utf-8'))
    conn = sqlite3.connect(args.db)
    try:
        sql = f"INSERT OR REPLACE INTO rides ({', '.join(FIELDS)}) VALUES ({', '.join('?' for _ in FIELDS)})"
        for row in rides:
            ride = row.get('ride') or {}
            src = row.get('source') or {}
            values = [
                row.get('provider'), src.get('gmail_message_id'), src.get('email_date'), src.get('subject'),
                ride.get('start_time_text'), ride.get('end_time_text'), ride.get('total_text'), ride.get('currency'), ride.get('amount'),
                ride.get('pickup'), ride.get('dropoff'), ride.get('pickup_city'), ride.get('pickup_country'), ride.get('dropoff_city'), ride.get('dropoff_country'),
                ride.get('payment_method'), ride.get('driver'), ride.get('distance_text'), ride.get('duration_text'), ride.get('notes'),
                json.dumps(row, ensure_ascii=False),
            ]
            conn.execute(sql, values)
        conn.commit()
    finally:
        conn.close()

    print(f'Inserted {len(rides)} rides into {args.db}')


if __name__ == '__main__':
    main()
