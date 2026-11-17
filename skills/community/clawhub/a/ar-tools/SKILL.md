---
name: ar-tools
description: Validaciones y datos de Argentina para agentes (CUIT/CUIL, CBU/CVU, teléfonos, cotización del dólar). Usar cuando el usuario mencione un CUIT, CUIL, CBU, CVU, un teléfono argentino o pregunte el valor del dólar en Argentina. Servidor MCP remoto + REST; cobra por créditos prepagos con key de prueba gratis.
version: 0.1.1
author: Joaquín Torletti
metadata:
  openclaw:
    emoji: "🇦🇷"
    homepage: "https://ar-tools-api-103907796853.us-east1.run.app"
    envVars:
      - name: AR_TOOLS_API_KEY
        required: false
        description: "API key (ak_...). Si falta, pedí una gratis con POST https://ar-tools-api-103907796853.us-east1.run.app/v1/keys"
  hermes:
    tags: [argentina, cuit, cbu, dolar, fintech, mcp, latam]
---

# AR Tools

API de datos argentinos pensada para agentes. Un mismo backend se consume de tres formas:

| Puerta | URL | Cuándo usarla |
|---|---|---|
| MCP remoto (Streamable HTTP) | `https://ar-tools-api-103907796853.us-east1.run.app/mcp` | OpenClaw, Hermes, Claude, Cursor: cualquier cliente MCP |
| REST + OpenAPI | `https://ar-tools-api-103907796853.us-east1.run.app/openapi.json` | Agentes custom o cuando no hay cliente MCP |
| Esta skill | `https://ar-tools-api-103907796853.us-east1.run.app/skill.md` | Para saber cuándo y cómo llamar |

## Tools y costo

| Tool | Qué hace | Créditos |
|---|---|---|
| `validar_cuit` | Valida dígito verificador, devuelve tipo (física/jurídica) y formato `XX-XXXXXXXX-X` | 1 |
| `validar_cbu` | Valida CBU/CVU de 22 dígitos, identifica banco o billetera, sucursal y cuenta | 1 |
| `normalizar_telefono_ar` | Teléfono argentino en cualquier formato a E.164, WhatsApp y nacional; celular o fijo | 1 |
| `cotizacion_dolar` | Cotización actual compra/venta: oficial, blue, bolsa (MEP), contadoconliqui, mayorista, cripto, tarjeta | 2 |
| `ejecutar` | Code Mode: corre JavaScript contra `api.*` en sandbox; lotes y encadenados en una sola llamada | 1 + llamadas |

Solo se cobra una llamada exitosa. Un input inválido (CUIT mal formado) es una respuesta exitosa con `valido: false` y se cobra. Si falla un proveedor externo (502) no se cobra.

## Conseguir una API key

Sin registro. Pedí una key de prueba:

```bash
curl -X POST https://ar-tools-api-103907796853.us-east1.run.app/v1/keys -H 'content-type: application/json' -d '{"name":"mi-agente"}'
```

La respuesta trae `key` (empieza con `ak_`). Guardala: no se vuelve a mostrar. Enviala siempre como header `Authorization: Bearer ak_...`.

Cuando se acaben los créditos la API responde HTTP 402 con `checkout_url`. Mostrale esa URL al usuario para que recargue; no reintentes la llamada en loop.

### Comprar créditos

Hay packs de créditos (ver `GET https://ar-tools-api-103907796853.us-east1.run.app/v1/packs`). Para recargar la key del usuario:

- Por MCP: llamá a la tool `comprar_creditos` (sin costo); devuelve `checkout_url`.
- Por REST: `POST https://ar-tools-api-103907796853.us-east1.run.app/v1/checkout` con la key, body opcional `{"credits": 500}`; devuelve `checkout_url`.
- Un humano también puede abrir `https://ar-tools-api-103907796853.us-east1.run.app/comprar?key_id=<key_id>` (el `key_id` viene en el 402 y en `/v1/balance`).

Mostrá la `checkout_url` al usuario: paga con tarjeta en Polar y los créditos se acreditan solos en segundos. Después consultá `GET /v1/balance` y seguí.

## Configurar como servidor MCP

Agregá el servidor a la configuración MCP de tu agente. La forma genérica es:

```json
{
  "mcpServers": {
    "ar-tools": {
      "url": "https://ar-tools-api-103907796853.us-east1.run.app/mcp",
      "headers": { "Authorization": "Bearer ak_TU_KEY" }
    }
  }
}
```

Hermes y OpenClaw aceptan servidores MCP remotos con URL y headers; revisá en la documentación de tu agente el archivo exacto donde van (en Hermes es la sección de servidores MCP de su `config.yaml`; en OpenClaw, la configuración de MCP del agente). Una vez conectado, las cuatro tools aparecen junto a las nativas.

## Usar por REST

Cada tool es `POST https://ar-tools-api-103907796853.us-east1.run.app/v1/tools/<nombre>` con un JSON de entrada:

```bash
curl -X POST https://ar-tools-api-103907796853.us-east1.run.app/v1/tools/validar_cuit \
  -H 'Authorization: Bearer ak_TU_KEY' -H 'content-type: application/json' \
  -d '{"cuit":"30-50001091-2"}'
```

Respuesta:

```json
{ "result": { "valido": true, "cuit": "30500010912", "formateado": "30-50001091-2", "tipo": "persona_juridica", "prefijo": "30" },
  "credits": { "cost": 1, "balance": 49 } }
```

Saldo: `GET https://ar-tools-api-103907796853.us-east1.run.app/v1/balance` con la misma key.

## Code Mode: `ejecutar`

Para lotes o encadenar llamadas sin volver al modelo, mandá JavaScript a la tool `ejecutar`. El código corre en un sandbox con un objeto `api` ya autenticado: una función `async` por tool, con los mismos parámetros y el mismo resultado.

```js
const cuits = ['20-12345678-6', '30-50001091-2'];
const out = [];
for (const c of cuits) out.push(await api.validarCuit({ cuit: c }));
return out.filter(x => x.valido).map(x => x.formateado);
```

Funciones: `api.validarCuit`, `api.validarCbu`, `api.normalizarTelefonoAr`, `api.cotizacionDolar`. Podés usar `await`, `console.log` y `return`; el valor retornado vuelve en `resultado` y los logs en `logs`. Sin red, archivos ni módulos; máximo 100 llamadas y 15 segundos.

Costo: 1 crédito por ejecución más la suma de las llamadas internas. Si una llamada falla por saldo, lanza un error con `code = "insufficient_credits"` que podés atrapar. Preferí `ejecutar` cuando vayas a hacer más de 3 llamadas seguidas.

## Reglas para el agente

- Antes de validar un CUIT o CBU, no intentes calcular el dígito verificador vos: usá la tool, es más barata que equivocarse.
- Para el dólar, pedí solo la casa que necesitás (`casa: "blue"`) salvo que el usuario quiera comparar.
- Para más de 3 llamadas seguidas, usá `ejecutar` con un solo script.
- Si recibís `insufficient_credits`, llamá a `comprar_creditos` (o `POST /v1/checkout`), mostrá la `checkout_url` al usuario y esperá a que recargue; no reintentes en loop.
- Si recibís `upstream_error`, avisá que la fuente externa falló; podés reintentar una vez.
