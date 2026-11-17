CREATE TABLE orders (tenant_id TEXT, order_id INTEGER, customer_ref INTEGER,
 amount REAL, status TEXT, ordered_at TEXT, delivered_at TEXT,
 PRIMARY KEY (tenant_id, order_id));
CREATE TABLE customers (tenant_id TEXT, customer_id INTEGER, region TEXT,
 PRIMARY KEY (tenant_id, customer_id));
CREATE TABLE items (item_id INTEGER PRIMARY KEY, tenant_id TEXT, order_ref INTEGER);
