---
name: direcciones-ar
description: Direcciones argentinas para agentes con el callejero oficial (georef, INDEC/IGN): normalizar y geocodificar una dirección escrita a mano, geocodificación inversa lat/lon → provincia/partido/municipio, buscar calles y localidades, resolver provincias/departamentos/municipios con ids oficiales. Usar cuando el usuario pase una dirección de Argentina para validar, completar, geolocalizar o cargar en un formulario, o pregunte a qué partido/provincia pertenece un lugar. Servidor MCP remoto + REST; cobra por créditos prepagos con key de prueba gratis.
version: 0.1.1
author: Joaquín Torletti
metadata:
  openclaw:
    emoji: "📍"
    homepage: "https://direcciones-ar-api-103907796853.us-east1.run.app"
    envVars:
      - name: DIRECCIONES_AR_API_KEY
        required: false
        description: "API key (ak_...). Si falta, pedí una gratis con POST https://direcciones-ar-api-103907796853.us-east1.run.app/v1/keys"
  hermes:
    tags: [argentina, direcciones, geocoding, georef, logistica, ecommerce, mcp]
---

# Direcciones AR

Normalización y geocodificación de direcciones argentinas con el callejero oficial (georef: INDEC e IGN), listo para agentes. Un mismo backend se consume de tres formas:

| Puerta | URL | Cuándo usarla |
|---|---|---|
| MCP remoto (Streamable HTTP) | `https://direcciones-ar-api-103907796853.us-east1.run.app/mcp` | OpenClaw, Hermes, Claude, Cursor: cualquier cliente MCP |
| REST + OpenAPI | `https://direcciones-ar-api-103907796853.us-east1.run.app/openapi.json` | Agentes custom o sin cliente MCP |
| Esta skill | `https://direcciones-ar-api-103907796853.us-east1.run.app/skill.md` | Para saber cuándo y cómo llamar |

## Tools y costo

| Tool | Qué hace | Créditos |
|---|---|---|
| `normalizar_direccion` | Interpreta 'Av. Corrientes 1234, CABA' o 'corrientes y callao', la normaliza y devuelve candidatos con calle, altura, localidad, partido, provincia y lat/lon | 2 |
| `ubicacion` | Geocodificación inversa: lat/lon → provincia, departamento/partido y municipio con ids INDEC | 1 |
| `buscar_localidad` | Localidades por nombre aproximado con provincia, partido, municipio y centroide | 1 |
| `buscar_calle` | Calles por nombre aproximado: nombre oficial, categoría, rango de alturas y jurisdicción | 1 |
| `buscar_division` | Provincias, departamentos/partidos o municipios por nombre, con id oficial y centroide | 1 |
| `ejecutar` | Code Mode: corre JavaScript contra `api.*` en sandbox; lotes y encadenados en una sola llamada | 1 + llamadas |

Fuente: API georef del Estado argentino (datos de INDEC e IGN). No incluye código postal ni números de puerta inexistentes en el callejero. Solo se cobra la llamada exitosa; si la fuente falla (502) no se cobra.

## Conseguir una API key

Sin registro:

```bash
curl -X POST https://direcciones-ar-api-103907796853.us-east1.run.app/v1/keys -H 'content-type: application/json' -d '{"name":"mi-agente"}'
```

La respuesta trae `key` (empieza con `ak_`). Guardala y enviala siempre como header `Authorization: Bearer ak_...`. Sin créditos la API responde HTTP 402 con `checkout_url`: mostrásela al usuario y no reintentes en loop.

### Comprar créditos

Hay packs de créditos (ver `GET https://direcciones-ar-api-103907796853.us-east1.run.app/v1/packs`). Para recargar la key del usuario:

- Por MCP: llamá a la tool `comprar_creditos` (sin costo); devuelve `checkout_url`.
- Por REST: `POST https://direcciones-ar-api-103907796853.us-east1.run.app/v1/checkout` con la key, body opcional `{"credits": 500}`; devuelve `checkout_url`.
- Un humano también puede abrir `https://direcciones-ar-api-103907796853.us-east1.run.app/comprar?key_id=<key_id>` (el `key_id` viene en el 402 y en `/v1/balance`).

Mostrá la `checkout_url` al usuario: paga con tarjeta en Polar y los créditos se acreditan solos en segundos. Después consultá `GET /v1/balance` y seguí.

## Configurar como servidor MCP

```json
{
  "mcpServers": {
    "direcciones-ar": {
      "url": "https://direcciones-ar-api-103907796853.us-east1.run.app/mcp",
      "headers": { "Authorization": "Bearer ak_TU_KEY" }
    }
  }
}
```

## Usar por REST

```bash
curl -X POST https://direcciones-ar-api-103907796853.us-east1.run.app/v1/tools/normalizar_direccion \
  -H 'Authorization: Bearer ak_TU_KEY' -H 'content-type: application/json' \
  -d '{"direccion":"San Martín 450 piso 3","localidad":"Rosario","provincia":"Santa Fe"}'
```

## Code Mode: `ejecutar`

Para normalizar una lista de direcciones o encadenar búsquedas sin volver al modelo, mandá JavaScript a la tool `ejecutar`. El código corre en un sandbox con un objeto `api` ya autenticado: una función `async` por tool, con los mismos parámetros y el mismo resultado.

```js
const clientes = [
  { id: 1, dir: 'Av Corrientes 1234', prov: 'CABA' },
  { id: 2, dir: 'San Martín 450', prov: 'Santa Fe', loc: 'Rosario' },
];
const out = [];
for (const c of clientes) {
  const n = await api.normalizarDireccion({ direccion: c.dir, provincia: c.prov, localidad: c.loc, max: 1 });
  out.push({ id: c.id, ok: n.cantidad > 0, ambigua: n.ambigua, normalizada: n.mejor?.nomenclatura, lat: n.mejor?.lat, lon: n.mejor?.lon });
}
return out;
```

Funciones: `api.normalizarDireccion`, `api.ubicacion`, `api.buscarLocalidad`, `api.buscarCalle`, `api.buscarDivision`. Podés usar `await`, `console.log` y `return`; el valor retornado vuelve en `resultado` y los logs en `logs`. Sin red, archivos ni módulos; máximo 100 llamadas y 15 segundos.

Costo: 1 crédito por ejecución más la suma de las llamadas internas. Si una llamada falla por saldo, lanza un error con `code = "insufficient_credits"` que podés atrapar. Preferí `ejecutar` cuando vayas a hacer más de 3 llamadas seguidas.

## Reglas para el agente

- Pasá `provincia` y `localidad` siempre que el usuario las haya dicho: el callejero tiene muchas calles homónimas.
- Si `cantidad` es 0, la dirección no existe en el callejero oficial: no inventes coordenadas; pedí al usuario que revise calle o localidad, o probá `buscar_calle` para sugerir la calle correcta.
- Si `ambigua` es true, mostrá los `candidatos` con su localidad y dejá elegir; no asumas el primero sin decirlo.
- La `nomenclatura` es la forma oficial: usala para cargar formularios o etiquetas de envío.
- Para más de 3 direcciones, usá `ejecutar` con un solo script.
- Si recibís `insufficient_credits`, llamá a `comprar_creditos` (o `POST /v1/checkout`), mostrá la `checkout_url` al usuario y esperá a que recargue; no reintentes en loop. Si recibís `upstream_error`, avisá que la fuente falló; podés reintentar una vez.
