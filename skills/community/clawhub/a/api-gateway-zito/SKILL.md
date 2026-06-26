---
name: api-gateway
description: Gateway universal para APIs. Conecta cualquier API REST/GraphQL con configuración simple. Gestiona autenticación, rate limiting y caching.
metadata: {"openclaw":{"emoji":"🔌","auto":false}}
---

# API Gateway Universal

Conecta el bot a cualquier API externa con configuración mínima. Un solo lugar para gestionar todas tus integraciones.

## Concepto

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Bot      │ ──► │  API        │ ──► │  APIs       │
│  (Comando)  │     │  Gateway    │     │  Externas   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │ • Auth      │
                    │ • Cache     │
                    │ • Rate Limit│
                    │ • Retry     │
                    └─────────────┘
```

## Comandos

### Configurar APIs

```
# Agregar nueva API
api add weather
  --base:https://api.openweathermap.org/data/2.5
  --auth:query:appid:$WEATHER_API_KEY

# Agregar endpoint
api endpoint weather current
  --path:/weather
  --params:q,units

# Listar APIs configuradas
api list
```

### Llamar APIs

```
# Llamar endpoint
api call weather current --q:"Mexico City" --units:metric

# Llamada directa con URL
api get https://api.example.com/data

# POST con body
api post https://api.example.com/create --body:'{"name":"test"}'
```

### Gestión

```
# Ver estadísticas
api stats weather

# Ver logs
api logs --last:10

# Probar conexión
api test weather
```

## Ejemplo: Configurar API del Clima

```yaml
# apis/weather.yaml
name: weather
base_url: https://api.openweathermap.org/data/2.5
auth:
  type: query
  param: appid
  value: ${WEATHER_API_KEY}
  
endpoints:
  current:
    path: /weather
    method: GET
    params:
      - q: string  # ciudad
      - units: metric|imperial
    cache: 10m
    
  forecast:
    path: /forecast
    method: GET
    params:
      - q: string
      - cnt: number  # días
```

## Uso después de configurar

```
Usuario: clima en "Ciudad de México"

Bot: 🌤️ Clima actual en Ciudad de México:
     
     🌡️ Temperatura: 22°C
     💧 Humedad: 45%
     💨 Viento: 12 km/h
     🌅 Sensación térmica: 24°C
```

## Tipos de Autenticación

| Tipo | Ejemplo |
|------|---------|
| **API Key (Header)** | `Authorization: Bearer xxx` |
| **API Key (Query)** | `?api_key=xxx` |
| **Basic Auth** | `username:password` |
| **OAuth 2.0** | Token refresh automático |
| **Custom** | Headers personalizados |

## Funcionalidades

### Caching

```yaml
endpoints:
  data:
    cache: 15m  # Cache de 15 minutos
```

### Rate Limiting

```yaml
rate_limit:
  requests: 100
  period: 1h
```

### Retry Automático

```yaml
retry:
  attempts: 3
  backoff: exponential
```

## APIs Pre-configuradas

| API | Configuración |
|-----|---------------|
| OpenWeather | `WEATHER_API_KEY` |
| GitHub | `GITHUB_TOKEN` |
| Slack | `SLACK_TOKEN` |
| Notion | `NOTION_API_KEY` |
| Discord | `DISCORD_TOKEN` |

## Integración

- **proactive-triggers**: Llamar APIs en automatizaciones
- **daily-digest**: Obtener datos de múltiples APIs
- **multi-agent**: Los agentes pueden usar APIs configuradas
