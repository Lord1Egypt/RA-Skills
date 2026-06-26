import mysql.connector
from urllib.parse import urlparse, parse_qs
import os

# MySQL connection settings (can customize)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "test_db")

TABLE_NAME = "url_parameters"

def connect_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

def create_table_if_not_exists(columns):
    conn = connect_db()
    cursor = conn.cursor()

    # Build column definitions
    column_defs = ", ".join(f"{col} VARCHAR(255)" for col in columns)
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {column_defs}
    )
    """
    cursor.execute(create_sql)
    conn.commit()
    cursor.close()
    conn.close()

def save_url_params(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # Flatten values (take first value if multiple)
    flat_params = {k: v[0] for k, v in params.items()}

    if not flat_params:
        print("No parameters found in URL.")
        return

    # Create table with these columns if not exists
    create_table_if_not_exists(flat_params.keys())

    # Insert data
    conn = connect_db()
    cursor = conn.cursor()

    columns = ", ".join(flat_params.keys())
    placeholders = ", ".join(["%s"] * len(flat_params))
    values = list(flat_params.values())

    insert_sql = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})"
    cursor.execute(insert_sql, values)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted parameters into {TABLE_NAME}: {flat_params}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python save_url_params.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    save_url_params(url)