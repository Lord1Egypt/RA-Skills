# 🌤️ AEMET Skill for OpenClaw

Consulta alertas meteorológicas y predicciones de la Agencia Estatal de Meteorología (AEMET) de España directamente desde OpenClaw.

## ✨ Características

- **Alertas por nivel de color**: verde, amarillo, naranja, rojo
- **Predicciones diarias y horarias** para cualquier municipio español
- **Búsqueda inteligente**: por nombre o código postal
- **Cache inteligente**: 5 minutos para alertas, 24h para municipios
- **Manejo de rate limits**: retry automático con backoff
- **Parseo XML robusto** con xmllint
- **Validación de entrada** y mensajes de error claros

## 🚀 Instalación rápida

```bash
# Instalar dependencias
sudo apt update
sudo apt install -y curl jq libxml2-utils

# Configurar API key (gratuita)
echo "TU_API_KEY_AQUI" > ~/.openclaw/credentials/aemet-api-key.txt

# Probar la skill
aemet test
```

## 📋 Uso

### Alertas por área
```bash
# Alertas para Madrid
aemet alertas madrid

# Alertas filtradas por nivel
aemet alertas cataluña amarilla,naranja
```

### Predicciones por municipio
```bash
# Predicción diaria
aemet pronóstico 28001
aemet pronóstico "Madrid"

# Predicción horaria
aemet pronóstico "Barcelona" --horaria
```

### Búsqueda de municipios
```bash
# Buscar por nombre
aemet buscar "Madrid"

# Buscar por código postal
aemet buscar 28001
```

## 🗺️ Códigos de área

| Área | Código |
|------|--------|
| Andalucía | 1 |
| Aragón | 2 |
| Asturias | 3 |
| Baleares | 4 |
| Canarias | 5 |
| Cantabria | 6 |
| Castilla-La Mancha | 7 |
| Castilla y León | 8 |
| Cataluña | 9 |
| Comunidad Valenciana | 10 |
| Extremadura | 11 |
| Galicia | 12 |
| Madrid | 72 |
| Murcia | 13 |
| Navarra | 15 |
| País Vasco | 16 |
| La Rioja | 17 |
| Ceuta | 18 |
| Melilla | 19 |

## ⚠️ Limitaciones de la API AEMET

- **Rate limit**: 20 peticiones por minuto
- **URLs temporales**: Los datos tienen URLs con validez de 30 segundos
- **Actualización**: Alertas cada 5 min, predicciones varias veces al día
- **Formato**: Alertas en formato CAP XML complejo

## 🔧 Solución de problemas

### Error "429 Too Many Requests"
La skill incluye manejo automático de rate limits con:
- Cache para reducir peticiones
- Retry con backoff exponencial
- Mensajes claros cuando se supera el límite

### Error "No se encontró el municipio"
- Usa el nombre exacto (ej: "Madrid" no "madrid")
- Los códigos postales deben ser de 5 dígitos
- Prueba a buscar primero: `aemet buscar "nombre"`

### Error de parseo XML
- Asegúrate de tener `xmllint` instalado (`libxml2-utils`)
- La skill tiene fallback básico si falta xmllint

## 📄 Licencia

MIT License - Libre para uso personal y comercial.

## 👤 Autor

Pablo Martínez Crespo

## 🔗 Enlaces

- [AEMET OpenData](https://opendata.aemet.es/)
- [Registro API key](https://opendata.aemet.es/centrodedescargas/altaUsuario)
- [OpenClaw](https://openclaw.ai/)
- [ClawHub](https://clawhub.ai/)