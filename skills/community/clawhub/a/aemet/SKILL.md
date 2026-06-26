---
name: aemet
description: Weather alerts and forecasts from AEMET OpenData for Spain
---

# AEMET Skill

Consulta alertas meteorológicas y predicciones oficiales de AEMET OpenData para cualquier municipio de España.

## Requisitos previos

### 1. API Key de AEMET (gratuita)

1. Regístrate en https://opendata.aemet.es/
2. Una vez obtenida, guárdala en:

```
~/.openclaw/credentials/aemet-api-key.txt
```

```bash
echo "TU_CLAVE_AQUI" > ~/.openclaw/credentials/aemet-api-key.txt
chmod 600 ~/.openclaw/credentials/aemet-api-key.txt
```

### 2. Dependencias del sistema

```bash
sudo apt update
sudo apt install -y curl jq libxml2-utils coreutils
```

- `curl` — peticiones HTTP a la API de AEMET
- `jq` — parseo de JSON
- `xmllint` — parseo XML (opcional, fallback disponible)
- `md5sum` — cacheo de respuestas

## Uso

```bash
cd ~/.openclaw/workspace/skills/aemet

# Alertas meteorológicas por área (Madrid capital = área 72)
./aemet.sh alertas madrid
./aemet.sh alertas 72

# Predicción diaria de un municipio
./aemet.sh prediccion madrid

# Predicción horaria (24h)
./aemet.sh hourly madrid

# Buscar municipio por nombre
./aemet.sh search "Soria"

# Ayuda completa
./aemet.sh help
```

## Funcionalidades

- **Alertas**: Niveles de color (verde, amarillo, naranja, rojo) con descripción del fenómeno
- **Predicción diaria**: Temperatura máxima/mínima, estado del cielo, precipitación, viento
- **Predicción horaria**: Cada 3 horas durante 24h
- **Búsqueda de municipios**: Por nombre o código INE
- **Cacheo inteligente**: 5 minutos para alertas, 24h para municipios
- **Rate limits**: Pausa automática con backoff si AEMET limita

## Códigos de área frecuentes

| Ciudad          | Código |
|-----------------|--------|
| Madrid          | 72     |
| Valencia        | 94     |
| Barcelona       | 94     |
| Sevilla         | 91     |

Para otros municipios, usa `./aemet.sh search "nombre"` y anota el código de 4 dígitos.

## Rutas importantes

| Recurso               | Ruta                                          |
|-----------------------|-----------------------------------------------|
| API Key               | `~/.openclaw/credentials/aemet-api-key.txt`   |
| Cache alertas         | `~/.openclaw/cache/aemet/alertas_*`            |
| Cache municipios       | `~/.openclaw/cache/aemet/municipios_*`        |
| Script principal      | `~/.openclaw/workspace/skills/aemet/aemet.sh` |

## Limitaciones

- Rate limit: ~80 peticiones/minuto (impuesto por AEMET)
- La API key es personal — no subirla a repositorios públicos
- Datos: pronóstico hasta 7 días, histórico no disponible
