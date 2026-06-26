# Datasets Reference

## Public Electricity Load Datasets

### 1. UCI Electric Load Diagrams

**Description**: Hourly electricity consumption for 370 clients over 3.5 years.

**Source**: https://archive.ics.uci.edu/ml/datasets/ElectricLoadDiagrams20112014

**Details**:
- 370 residential/commercial clients
- Period: 2011-2014
- Resolution: Hourly
- Size: ~11 MB

**Use case**: Customer-level forecasting, clustering analysis

```python
import pandas as pd

# Load data
df = pd.read_csv('ElectricLoadDiagrams20112014.txt', sep=';')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
```

### 2. PJM Interconnection Load Data

**Description**: Real-time and historical load data for PJM grid (US East Coast).

**Source**: https://datatracker.pjm.com/

**Details**:
- Regional transmission organization
- Period: 1997-present
- Resolution: Hourly and 5-minute
- Coverage: 13 states + DC

**Use case**: Grid-level forecasting, price-load relationship

```python
# API access example
import requests

url = "https://api.pjm.com/api/v1/inst_load"
params = {
    'startDate': '20240101',
    'endDate': '20240131',
    'fields': 'datetime,load_mw'
}
headers = {'Ocp-Apim-Subscription-Key': 'YOUR_API_KEY'}

response = requests.get(url, params=params, headers=headers)
data = response.json()
```

### 3. ISO-NE Load Data

**Description**: New England grid operator load data.

**Source**: https://www.iso-ne.com/isoexpress/

**Details**:
- New England region (6 states)
- Period: 2003-present
- Resolution: Hourly
- Includes: Load, temperature, fuel mix

**Use case**: Regional forecasting, weather-load analysis

### 4. ERCOT Load Data

**Description**: Texas grid operator load and generation data.

**Source**: https://www.ercot.com/gridinfo/load

**Details**:
- Texas grid (isolated from US interconnects)
- Period: 2000-present
- Resolution: 5-minute and hourly
- Includes: Load, wind, solar generation

**Use case**: Renewable integration studies, extreme weather analysis

### 5. UK National Grid ESO

**Description**: UK electricity system operator data.

**Source**: https://data.nationalgrideso.com/

**Details**:
- Great Britain grid
- Period: 2000-present
- Resolution: Half-hourly (Settlement Periods)
- Includes: Demand, generation, frequency

**Use case**: European market analysis, demand response studies

```python
# Using their API
import requests

url = "https://data.nationalgrideso.com/dataset/3f6a1f81-0e6b-4310-8c1f-7e8c5e8b5c5a"
# Download and parse CSV
```

### 6. Australian NEM Data

**Description**: National Electricity Market (Australia) data.

**Source**: https://www.aemo.com.au/energy-electricity-national-electricity-market-nem/data-nem

**Details**:
- Australian National Electricity Market
- Resolution: 5-minute intervals
- Includes: Demand, price, generation by fuel type

**Use case**: Market analysis, renewable integration

### 7. ENTSO-E Transparency Platform

**Description**: European Network of Transmission System Operators data.

**Source**: https://transparency.entsoe.eu/

**Details**:
- Pan-European coverage
- Resolution: Hourly
- Includes: Load, generation, cross-border flows, prices

**Use case**: Multi-country analysis, European market studies

```python
# Using entsoe-py library
from entsoe import EntsoePandasClient
import pandas as pd

client = EntsoePandasClient(api_key='YOUR_API_KEY')

start = pd.Timestamp('20240101', tz='Europe/Brussels')
end = pd.Timestamp('20240201', tz='Europe/Brussels')

# Get load for Germany
load_de = client.query_load('DE_LU', start=start, end=end)
```

### 8. China National Data (Limited Public Access)

**Description**: China electricity data (limited public availability).

**Sources**:
- National Energy Administration: http://www.nea.gov.cn/
- State Grid Corporation: http://www.sgcc.com.cn/
- Provincial grid companies

**Details**:
- Monthly provincial data publicly available
- Hourly data typically requires partnership
- Rapidly growing renewable capacity

**Use case**: Asian market analysis, large-scale grid studies

### 9. Kaggle Datasets

**Description**: Community-contributed electricity datasets.

**Notable datasets**:
- "Hourly Energy Consumption" (PJME)
- "Short-term Load Forecasting" competitions
- "Smart Grid Data" collections

**Source**: https://www.kaggle.com/datasets?search=electricity+load

### 10. UCI Individual Household Electric Power Consumption

**Description**: Single household minute-level consumption.

**Source**: https://archive.ics.uci.edu/ml/datasets/Individual+household+electric+power+consumption

**Details**:
- One household in France
- Period: 2006-2010
- Resolution: Minute-level
- Size: ~130 MB

**Use case**: Residential load modeling, appliance-level analysis

```python
df = pd.read_csv('household_power_consumption.txt', sep=';', 
                 parse_dates={'timestamp': ['Date', 'Time']},
                 low_memory=False)
df.set_index('timestamp', inplace=True)
```

## Weather Data Sources

### 1. OpenWeatherMap

**API**: https://openweathermap.org/api

**Features**:
- Historical weather data
- Forecast data (up to 16 days)
- Global coverage
- Free tier: 1000 calls/day

```python
import requests

url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
params = {
    'lat': 39.9042,
    'lon': 116.4074,
    'dt': 1704067200,  # Unix timestamp
    'appid': 'YOUR_API_KEY',
    'units': 'metric'
}

response = requests.get(url, params=params)
weather = response.json()
```

### 2. WeatherAPI

**API**: https://www.weatherapi.com/

**Features**:
- Historical data (back to 2008)
- Forecast data
- Astronomy data

### 3. NOAA (US Focus)

**API**: https://www.ncdc.noaa.gov/cdo-web/webservices/v2

**Features**:
- Comprehensive US weather data
- Free access
- Multiple stations

### 4. ECMWF ERA5 Reanalysis

**Source**: https://cds.climate.copernicus.eu/

**Features**:
- Global historical weather
- High resolution
- Free for research

## Data Quality Considerations

### Missing Data Handling

```python
def handle_missing_load(df, max_gap_hours=4):
    """
    Handle missing values in load data.
    
    - Short gaps (<4h): Linear interpolation
    - Medium gaps (4-24h): Same hour previous day
    - Long gaps (>24h): Flag for manual review
    """
    df = df.copy()
    
    # Identify gaps
    missing_mask = df['load'].isna()
    gap_id = (~missing_mask).cumsum()
    gap_sizes = missing_mask.groupby(gap_id).transform('sum')
    
    # Short gaps: interpolate
    short_gaps = missing_mask & (gap_sizes <= max_gap_hours)
    df.loc[short_gaps, 'load'] = df['load'].interpolate(method='linear')
    
    # Medium gaps: use same hour previous day
    medium_gaps = missing_mask & (gap_sizes > max_gap_hours) & (gap_sizes <= 24)
    for idx in df[medium_gaps].index:
        prev_day = idx - pd.Timedelta(days=1)
        if prev_day in df.index and not pd.isna(df.loc[prev_day, 'load']):
            df.loc[idx, 'load'] = df.loc[prev_day, 'load']
    
    # Long gaps: flag
    long_gaps = missing_mask & (gap_sizes > 24)
    df.loc[long_gaps, 'load_quality_flag'] = 'MISSING_LONG_GAP'
    
    return df
```

### Outlier Detection

```python
def detect_load_outliers(df, method='iqr', window=168):
    """
    Detect outliers in load data.
    
    Methods:
    - 'iqr': Interquartile range
    - 'zscore': Z-score based
    - 'rolling': Rolling statistics
    """
    df = df.copy()
    
    if method == 'iqr':
        Q1 = df['load'].quantile(0.25)
        Q3 = df['load'].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 3 * IQR
        upper = Q3 + 3 * IQR
        df['outlier'] = (df['load'] < lower) | (df['load'] > upper)
    
    elif method == 'rolling':
        rolling_mean = df['load'].rolling(window=window, center=True).mean()
        rolling_std = df['load'].rolling(window=window, center=True).std()
        z_score = (df['load'] - rolling_mean) / rolling_std
        df['outlier'] = z_score.abs() > 4
    
    return df
```

### Data Validation Checklist

- [ ] No negative load values (unless net metering)
- [ ] No unrealistic spikes (>3x typical peak)
- [ ] No extended flat lines (sensor stuck)
- [ ] Timestamps continuous (no gaps)
- [ ] Timezone consistent
- [ ] DST transitions handled correctly
- [ ] Weather data aligned with load timestamps

## Sample Data Generation

For testing when real data unavailable:

```python
def generate_synthetic_load(n_days=365, seed=42):
    """
    Generate synthetic hourly electricity load data.
    
    Includes:
    - Daily seasonality (peaks morning/evening)
    - Weekly seasonality (lower on weekends)
    - Yearly seasonality (heating/cooling)
    - Temperature correlation
    - Random noise
    """
    np.random.seed(seed)
    
    # Create time index
    dates = pd.date_range('2024-01-01', periods=n_days*24, freq='H')
    df = pd.DataFrame(index=dates)
    
    # Base load (MW)
    base_load = 1000
    
    # Daily pattern (double peak)
    hour = df.index.hour
    daily_pattern = (
        0.8 +  # Base
        0.15 * np.sin(2 * np.pi * (hour - 8) / 24) +  # Morning peak
        0.2 * np.sin(2 * np.pi * (hour - 20) / 24)    # Evening peak
    )
    
    # Weekly pattern
    dow = df.index.dayofweek
    weekly_pattern = np.where(dow < 5, 1.0, 0.85)  # Weekend reduction
    
    # Yearly pattern (heating/cooling)
    doy = df.index.dayofyear
    yearly_pattern = 1 + 0.1 * np.cos(2 * np.pi * (doy - 15) / 365)
    
    # Temperature (synthetic)
    temp = 15 + 10 * np.sin(2 * np.pi * (doy - 100) / 365)  # Seasonal
    temp += 5 * np.sin(2 * np.pi * hour / 24)  # Daily variation
    temp += np.random.normal(0, 2, len(df))  # Noise
    
    # Temperature-load relationship (U-shaped)
    temp_effect = 0.02 * (temp - 18) ** 2
    
    # Combine
    load = base_load * daily_pattern * weekly_pattern * yearly_pattern * (1 + temp_effect)
    load += np.random.normal(0, 30, len(df))  # Random noise
    
    # Add some anomalies
    anomaly_days = np.random.choice(n_days, 5, replace=False)
    for day in anomaly_days:
        day_start = day * 24
        load[day_start:day_start+24] *= np.random.uniform(0.7, 1.3)
    
    df['load'] = load
    df['temperature'] = temp
    
    return df

# Generate and save
synthetic_data = generate_synthetic_load()
synthetic_data.to_csv('synthetic_load.csv')
```

## Data Licensing Notes

- **Grid operator data**: Typically free for research, check terms for commercial use
- **Weather APIs**: Free tiers usually sufficient for development
- **Commercial datasets**: May require licensing (e.g., Refinitiv, Bloomberg)
- **Academic datasets**: Usually free for research (cite appropriately)

Always verify:
1. Permitted use cases (research vs commercial)
2. Attribution requirements
3. Redistribution restrictions
4. Data update frequency
