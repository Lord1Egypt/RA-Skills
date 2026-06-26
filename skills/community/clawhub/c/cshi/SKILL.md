---
name: url-parameter-saver
description: extract parameters from a given URL and save them into a MySQL database. use when you need to store URL query parameters for later processing or analysis.
---

# URL Parameter Saver

This skill extracts parameters from a provided URL and saves them into a MySQL database. If the table does not exist, it will be created automatically. Currently supports single URL processing.

## Usage

1. Call the `save_url_params.py` script with a URL.
2. The script parses the query parameters and inserts them as a new row in the database.
3. Each URL's parameters are saved in independent rows.

### Database

- Database type: MySQL
- Table name: `url_parameters`
- Columns: dynamically matched to URL parameter names