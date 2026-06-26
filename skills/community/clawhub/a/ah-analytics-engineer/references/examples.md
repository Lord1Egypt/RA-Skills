# Analytics Engineer — Code Examples

## Example 1

```yaml
# dbt_project.yml
name: 'analytics_project'
version: '1.0.0'
config-version: 2

profile: 'analytics_project'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  analytics_project:
    +materialized: table
    staging:
      +materialized: view
      +docs:
        node_color: "lightblue"
    intermediate:
      +materialized: ephemeral
      +docs:
        node_color: "orange"
    marts:
      +materialized: table
      +docs:
        node_color: "lightgreen"
      core:
        +materialized: table
      finance:
        +materialized: table
      marketing:
        +materialized: table

vars:
  start_date: '2020-01-01'
  timezone: 'UTC'
  
seeds:
  analytics_project:
    +column_types:
      id: varchar(50)
      created_at: timestamp
```

## Example 2

```sql
-- models/staging/stg_customers.sql
{{
    config(
        materialized='view',
        tags=['staging', 'customers']
    )
}}

with source_data as (
    select * from {{ source('raw_data', 'customers') }}
),

cleaned_data as (
    select
        customer_id::varchar as customer_id,
        lower(trim(email)) as email,
        lower(trim(first_name)) as first_name,
        lower(trim(last_name)) as last_name,
        phone_number,
        created_at::timestamp as created_at,
        updated_at::timestamp as updated_at,
        is_active::boolean as is_active,
        
        -- Data quality flags
        case 
            when email is null or email = '' then false
            when email not like '%@%' then false
            else true
        end as has_valid_email,
        
        case
            when first_name is null or first_name = '' then false
            when last_name is null or last_name = '' then false
            else true
        end as has_valid_name

    from source_data
    where customer_id is not null
)

select * from cleaned_data

-- Generic tests in schema.yml
version: 2

sources:
  - name: raw_data
    description: Raw data from operational systems
    tables:
      - name: customers
        description: Customer data from CRM
        columns:
          - name: customer_id
            description: Unique customer identifier
            tests:
              - not_null
              - unique

models:
  - name: stg_customers
    description: Cleaned and standardized customer data
    columns:
      - name: customer_id
        description: Unique customer identifier
        tests:
          - not_null
          - unique
      - name: email
        description: Customer email address
        tests:
          - not_null
      - name: has_valid_email
        description: Flag indicating if email format is valid
        tests:
          - accepted_values:
              values: [true, false]
```

## Example 3

```sql
-- models/marts/core/dim_customers.sql
{{
    config(
        materialized='table',
        indexes=[
            {'columns': ['customer_key'], 'unique': True},
            {'columns': ['customer_id'], 'unique': True},
            {'columns': ['email']},
        ]
    )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

customer_metrics as (
    select 
        customer_id,
        count(*) as total_orders,
        sum(order_amount) as lifetime_value,
        max(order_date) as last_order_date,
        min(order_date) as first_order_date
    from {{ ref('stg_orders') }}
    group by customer_id
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key(['c.customer_id']) }} as customer_key,
        c.customer_id,
        c.email,
        c.first_name,
        c.last_name,
        c.phone_number,
        c.created_at,
        c.is_active,
        
        -- Customer segmentation
        case
            when cm.lifetime_value >= 1000 then 'High Value'
            when cm.lifetime_value >= 500 then 'Medium Value'
            when cm.lifetime_value >= 100 then 'Low Value'
            else 'New Customer'
        end as customer_segment,
        
        case
            when cm.last_order_date >= current_date - interval '30 days' then 'Active'
            when cm.last_order_date >= current_date - interval '90 days' then 'At Risk'
            when cm.last_order_date >= current_date - interval '365 days' then 'Dormant'
            else 'Churned'
        end as customer_status,
        
        coalesce(cm.total_orders, 0) as total_orders,
        coalesce(cm.lifetime_value, 0) as lifetime_value,
        cm.first_order_date,
        cm.last_order_date,
        
        current_timestamp as updated_at
        
    from customers c
    left join customer_metrics cm 
        on c.customer_id = cm.customer_id
    where c.has_valid_email = true
      and c.has_valid_name = true
)

select * from final

-- models/marts/core/fct_orders.sql
{{
    config(
        materialized='table',
        partition_by={
            "field": "order_date",
            "data_type": "date",
            "granularity": "month"
        },
        cluster_by=["customer_id", "order_date"]
    )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('dim_customers') }}
),

products as (
    select * from {{ ref('dim_products') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key(['o.order_id']) }} as order_key,
        c.customer_key,
        o.order_id,
        o.customer_id,
        o.order_date,
        o.order_status,
        
        -- Order metrics
        count(oi.order_item_id) as total_items,
        sum(oi.quantity) as total_quantity,
        sum(oi.unit_price * oi.quantity) as gross_amount,
        sum(oi.discount_amount) as total_discount,
        sum((oi.unit_price * oi.quantity) - oi.discount_amount) as net_amount,
        
        -- Time dimensions
        extract(year from o.order_date) as order_year,
        extract(month from o.order_date) as order_month,
        extract(quarter from o.order_date) as order_quarter,
        extract(dayofweek from o.order_date) as order_day_of_week,
        
        current_timestamp as updated_at
        
    from orders o
    inner join customers c on o.customer_id = c.customer_id
    inner join order_items oi on o.order_id = oi.order_id
    group by 1, 2, 3, 4, 5, 6, 10, 11, 12, 13
)

select * from final
```

## Example 4

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}

-- macros/audit_columns.sql
{% macro audit_columns() %}
    current_timestamp as created_at,
    current_timestamp as updated_at,
    '{{ this.identifier }}' as source_table
{% endmacro %}

-- macros/get_column_values_with_threshold.sql
{% macro get_column_values_with_threshold(table, column, threshold=0.01) %}
    {%- call statement('get_column_values', fetch_result=True) -%}
        with value_counts as (
            select 
                {{ column }},
                count(*) as count,
                count(*) / sum(count(*)) over() as percentage
            from {{ table }}
            group by {{ column }}
        )
        select {{ column }}
        from value_counts
        where percentage >= {{ threshold }}
        order by count desc
    {%- endcall -%}
    
    {%- set results = load_result('get_column_values') -%}
    {%- set values = results['data'] | map(attribute=0) | list -%}
    {{ return(values) }}
{% endmacro %}

-- macros/test_not_null_proportion.sql
{% test not_null_proportion(model, column_name, at_least=0.95) %}
    with validation as (
        select
            sum(case when {{ column_name }} is not null then 1 else 0 end) as not_null_count,
            count(*) as total_count
        from {{ model }}
    ),
    
    validation_summary as (
        select
            not_null_count,
            total_count,
            not_null_count / total_count as not_null_proportion
        from validation
    )
    
    select *
    from validation_summary
    where not_null_proportion < {{ at_least }}
{% endtest %}

-- macros/pivot.sql
{% macro pivot(column, values, agg='sum', then_value=1) %}
    {% for value in values %}
        {{ agg }}(
            case when {{ column }} = '{{ value }}' 
            then {{ then_value }} 
            else 0 end
        ) as {{ value }}
        {%- if not loop.last -%},{%- endif -%}
    {% endfor %}
{% endmacro %}
```

## Example 5

```sql
-- tests/generic/test_freshness.sql
{% test freshness(model, column_name, max_age_hours=24) %}
    select *
    from {{ model }}
    where {{ column_name }} < current_timestamp - interval '{{ max_age_hours }} hours'
{% endtest %}

-- tests/generic/test_expression_is_true.sql
{% test expression_is_true(model, expression) %}
    select *
    from {{ model }}
    where not ({{ expression }})
{% endtest %}

-- models/marts/core/schema.yml
version: 2

models:
  - name: fct_orders
    description: Order fact table with metrics and dimensions
    tests:
      - dbt_utils.equal_rowcount:
          compare_model: ref('stg_orders')
      - freshness:
          column_name: updated_at
          max_age_hours: 2
    columns:
      - name: order_key
        description: Surrogate key for orders
        tests:
          - not_null
          - unique
      - name: customer_key
        description: Foreign key to customer dimension
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_key
      - name: net_amount
        description: Net order amount after discounts
        tests:
          - not_null
          - expression_is_true:
              expression: "net_amount >= 0"
      - name: total_quantity
        description: Total items in order
        tests:
          - not_null_proportion:
              at_least: 0.99
          - expression_is_true:
              expression: "total_quantity > 0"
```

## Example 6

```yaml
# models/staging/sources.yml
version: 2

sources:
  - name: raw_data
    description: Raw operational data
    meta:
      owner: "@data-team"
      contains_pii: true
    tables:
      - name: customers
        description: Customer master data
        meta:
          update_frequency: "hourly"
          row_count: 50000
        columns:
          - name: customer_id
            description: Unique identifier for customer
            meta:
              dimension: true
          - name: email
            description: Customer email address
            meta:
              contains_pii: true
          - name: created_at
            description: Account creation timestamp
            meta:
              dimension: true
        tests:
          - dbt_utils.source_freshness:
              loaded_at_field: updated_at
              warn_after: {count: 2, period: hour}
              error_after: {count: 6, period: hour}

exposures:
  - name: customer_dashboard
    description: Executive dashboard showing customer metrics
    type: dashboard
    url: https://bi.company.com/dashboards/customers
    maturity: high
    owner:
      name: Business Intelligence Team
      email: bi-team@company.com
    depends_on:
      - ref('dim_customers')
      - ref('fct_orders')
    tags: ['executive', 'customers']
  
  - name: weekly_revenue_report
    description: Automated weekly revenue report
    type: ml
    owner:
      name: Finance Team
      email: finance@company.com
    depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
    tags: ['finance', 'automated']
```

## Example 7

```sql
-- models/marts/analytics/customer_cohort_analysis.sql
{{
    config(
        materialized='table',
        tags=['analytics', 'cohorts']
    )
}}

with customer_orders as (
    select
        customer_id,
        order_date,
        net_amount,
        row_number() over (partition by customer_id order by order_date) as order_sequence
    from {{ ref('fct_orders') }}
),

first_orders as (
    select
        customer_id,
        order_date as first_order_date,
        date_trunc('month', order_date) as cohort_month
    from customer_orders
    where order_sequence = 1
),

customer_monthly_activity as (
    select
        co.customer_id,
        fo.cohort_month,
        date_trunc('month', co.order_date) as order_month,
        sum(co.net_amount) as monthly_revenue
    from customer_orders co
    inner join first_orders fo on co.customer_id = fo.customer_id
    group by 1, 2, 3
),

cohort_analysis as (
    select
        cohort_month,
        order_month,
        datediff('month', cohort_month, order_month) as period_number,
        count(distinct customer_id) as customers,
        sum(monthly_revenue) as revenue
    from customer_monthly_activity
    group by 1, 2, 3
),

cohort_sizes as (
    select
        cohort_month,
        count(distinct customer_id) as cohort_size
    from first_orders
    group by 1
)

select
    ca.cohort_month,
    ca.period_number,
    ca.customers,
    cs.cohort_size,
    ca.customers / cs.cohort_size::float as retention_rate,
    ca.revenue,
    ca.revenue / ca.customers as revenue_per_customer
from cohort_analysis ca
inner join cohort_sizes cs on ca.cohort_month = cs.cohort_month
order by ca.cohort_month, ca.period_number

-- models/marts/analytics/customer_lifetime_value.sql
{{
    config(
        materialized='table',
        tags=['analytics', 'clv']
    )
}}

with customer_metrics as (
    select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        count(*) as total_orders,
        sum(net_amount) as total_revenue,
        avg(net_amount) as avg_order_value,
        datediff('day', min(order_date), max(order_date)) / nullif(count(*) - 1, 0) as avg_days_between_orders
    from {{ ref('fct_orders') }}
    group by customer_id
),

clv_calculation as (
    select
        customer_id,
        first_order_date,
        last_order_date,
        total_orders,
        total_revenue,
        avg_order_value,
        avg_days_between_orders,
        
        -- Purchase frequency (orders per year)
        case 
            when avg_days_between_orders > 0 then 365.0 / avg_days_between_orders
            else total_orders
        end as purchase_frequency,
        
        -- Customer lifespan in years
        case
            when datediff('day', first_order_date, last_order_date) > 0 
            then datediff('day', first_order_date, last_order_date) / 365.0
            else 1.0 / 365.0  -- Minimum of 1 day
        end as customer_lifespan,
        
        total_revenue as historical_clv
    from customer_metrics
),

final as (
    select
        *,
        avg_order_value * purchase_frequency * customer_lifespan as predicted_clv,
        case
            when predicted_clv >= 1000 then 'High Value'
            when predicted_clv >= 500 then 'Medium Value'
            when predicted_clv >= 100 then 'Low Value'
            else 'Minimal Value'
        end as clv_segment
    from clv_calculation
)

select * from final
```

## Example 8

```python
# Python script for automated BI refresh
import requests
import json
from datetime import datetime, timedelta
import logging

class BIRefreshManager:
    def __init__(self, tableau_server_url, username, password):
        self.server_url = tableau_server_url
        self.username = username
        self.password = password
        self.auth_token = None
        self.site_id = None
    
    def authenticate(self):
        """Authenticate with Tableau Server"""
        auth_url = f"{self.server_url}/api/3.10/auth/signin"
        
        payload = {
            'credentials': {
                'name': self.username,
                'password': self.password,
                'site': {'contentUrl': ''}
            }
        }
        
        response = requests.post(auth_url, json=payload)
        response.raise_for_status()
        
        auth_data = response.json()
        self.auth_token = auth_data['credentials']['token']
        self.site_id = auth_data['credentials']['site']['id']
        
        return self.auth_token
    
    def refresh_datasource(self, datasource_id):
        """Refresh a specific datasource"""
        headers = {
            'X-Tableau-Auth': self.auth_token,
            'Content-Type': 'application/json'
        }
        
        refresh_url = f"{self.server_url}/api/3.10/sites/{self.site_id}/datasources/{datasource_id}/refresh"
        
        response = requests.post(refresh_url, headers=headers)
        response.raise_for_status()
        
        job_data = response.json()
        return job_data['job']['id']
    
    def check_job_status(self, job_id):
        """Check the status of a refresh job"""
        headers = {'X-Tableau-Auth': self.auth_token}
        
        status_url = f"{self.server_url}/api/3.10/sites/{self.site_id}/jobs/{job_id}"
        
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        
        job_data = response.json()
        return job_data['job']['finishCode']

# dbt run automation with BI refresh
def run_dbt_and_refresh_bi():
    """Run dbt models and refresh BI dashboards"""
    import subprocess
    
    try:
        # Run dbt
        dbt_result = subprocess.run(['dbt', 'run'], capture_output=True, text=True)
        
        if dbt_result.returncode == 0:
            logging.info("dbt run completed successfully")
            
            # Run tests
            test_result = subprocess.run(['dbt', 'test'], capture_output=True, text=True)
            
            if test_result.returncode == 0:
                logging.info("All tests passed")
                
                # Refresh BI dashboards
                bi_manager = BIRefreshManager(
                    tableau_server_url="https://tableau.company.com",
                    username="analytics_service",
                    password="secure_password"
                )
                
                bi_manager.authenticate()
                job_id = bi_manager.refresh_datasource("datasource-id-123")
                
                logging.info(f"BI refresh started with job ID: {job_id}")
                
            else:
                logging.error(f"dbt tests failed: {test_result.stderr}")
                
        else:
            logging.error(f"dbt run failed: {dbt_result.stderr}")
            
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
```

## Example 9

```yaml
# .github/workflows/dbt_ci.yml
name: dbt CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  DBT_PROFILES_DIR: .
  DBT_PROFILE: analytics_project

jobs:
  dbt-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install dbt-snowflake
        pip install sqlfluff
        pip install great-expectations
    
    - name: Lint SQL
      run: |
        sqlfluff lint models/ --dialect snowflake
    
    - name: dbt deps
      run: dbt deps
    
    - name: dbt seed
      run: dbt seed --target ci
    
    - name: dbt run
      run: dbt run --target ci
    
    - name: dbt test
      run: dbt test --target ci
    
    - name: Generate dbt docs
      run: |
        dbt docs generate --target ci
        dbt docs serve --port 8080 &
        sleep 10
        curl http://localhost:8080
    
    - name: Data quality checks
      run: |
        python scripts/run_data_quality_checks.py

  deploy:
    needs: dbt-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        dbt run --target prod
        dbt test --target prod
        dbt docs generate --target prod
```

## Example 10

```python
# scripts/data_monitoring.py
import pandas as pd
import snowflake.connector
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MimeText

class DataMonitor:
    def __init__(self, connection_params):
        self.conn = snowflake.connector.connect(**connection_params)
    
    def check_data_freshness(self, table_name, timestamp_column, max_age_hours=2):
        """Check if data is fresh enough"""
        query = f"""
        SELECT 
            MAX({timestamp_column}) as latest_timestamp,
            DATEDIFF('hour', MAX({timestamp_column}), CURRENT_TIMESTAMP()) as hours_old
        FROM {table_name}
        """
        
        result = pd.read_sql(query, self.conn)
        hours_old = result['HOURS_OLD'].iloc[0]
        
        if hours_old > max_age_hours:
            self.send_alert(
                f"Data freshness alert for {table_name}",
                f"Data is {hours_old} hours old, exceeding threshold of {max_age_hours} hours"
            )
            return False
        return True
    
    def check_row_count_anomaly(self, table_name, threshold_percent=20):
        """Check for unusual row count changes"""
        query = f"""
        WITH daily_counts AS (
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as row_count
            FROM {table_name}
            WHERE created_at >= CURRENT_DATE - 7
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        ),
        count_comparison AS (
            SELECT 
                date,
                row_count,
                LAG(row_count) OVER (ORDER BY date) as prev_row_count,
                (row_count - LAG(row_count) OVER (ORDER BY date)) / LAG(row_count) OVER (ORDER BY date) * 100 as percent_change
            FROM daily_counts
        )
        SELECT * FROM count_comparison
        WHERE date = CURRENT_DATE - 1
        """
        
        result = pd.read_sql(query, self.conn)
        
        if not result.empty:
            percent_change = abs(result['PERCENT_CHANGE'].iloc[0])
            
            if percent_change > threshold_percent:
                self.send_alert(
                    f"Row count anomaly for {table_name}",
                    f"Row count changed by {percent_change:.1f}% from previous day"
                )
                return False
        return True
    
    def send_alert(self, subject, message):
        """Send email alert"""
        msg = MimeText(message)
        msg['Subject'] = subject
        msg['From'] = 'data-alerts@company.com'
        msg['To'] = 'data-team@company.com'
        
        with smtplib.SMTP('smtp.company.com') as server:
            server.send_message(msg)

# Usage
monitor = DataMonitor({
    'user': 'analytics_user',
    'password': 'secure_password',
    'account': 'company_account',
    'warehouse': 'ANALYTICS_WH',
    'database': 'ANALYTICS_DB',
    'schema': 'MARTS'
})

# Run monitoring checks
tables_to_monitor = [
    'dim_customers',
    'fct_orders',
    'fct_web_events'
]

for table in tables_to_monitor:
    monitor.check_data_freshness(table, 'updated_at')
    monitor.check_row_count_anomaly(table)
```
