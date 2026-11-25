CREATE TABLE company (
  id TEXT PRIMARY KEY,
  status TEXT
);
CREATE TABLE vehicle (
  id TEXT PRIMARY KEY,
  company_id TEXT,
  abnormal INTEGER,
  FOREIGN KEY (company_id) REFERENCES company(id)
);
