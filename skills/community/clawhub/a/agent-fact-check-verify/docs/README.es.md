# Agent Fact Check Verify

**Selector de idioma**: [中文](../README.md) | [English](README.en.md) | **Español (actual)** | [العربية](README.ar.md)

Versión: **1.0.5**  
Autor: **Allen Niu**  
Licencia: **MIT**

`agent-fact-check-verify` es una habilidad de verificación rigurosa para agentes de IA. Extrae afirmaciones verificables, realiza verificación cruzada multi‑fuente (oficial, medios principales, sitios de fact-check y señales sociales), aplica reglas internas deterministas y entrega una respuesta neutral e integrada sin mostrar puntuaciones internas al usuario.

---

## 1. Objetivos de diseño y principios profesionales

Esta habilidad está construida para flujos auditables y reproducibles, no para textos “que suenan convincentes”.

- **Reproducible**: misma evidencia, misma decisión.
- **Trazable**: cada conclusión se vincula con fuentes.
- **Auditable**: reglas internas fijas; sin puntuación arbitraria.
- **Neutral**: redacción sin postura política.
- **Costo acotado**: presupuesto de búsquedas por afirmación.

---

## 2. Alcance (qué hace / qué no hace)

### Frases de activación (recomendado)

Si el usuario escribe “verificar”, “fact-check”, “¿es cierto?”, “核實” o “核實這個”, esta skill debe activarse primero.

### 2.1 Incluye

1. Extracción de afirmaciones desde texto largo.
2. Clasificación de tipo: statistical / causal / attribution / event / prediction / opinion / satire.
3. Verificación en tres rondas: oficial → mainstream → contraevidencia.
4. Decisión interna determinista por bandas.
5. Respuesta integrada al usuario sin mostrar puntuación.

### 2.2 Excluye

1. No fuerza veredicto verdadero/falso para opiniones puras.
2. No toma volumen social como prueba principal.
3. No usa lenguaje de persuasión política.
4. No garantiza cobertura de material privado o de pago.

---

## 3. Estructura del proyecto

```text
agent-fact-check-verify/
├── SKILL.md
├── LICENSE
├── README.md                    # Chino por defecto
├── scripts/
│   └── factcheck_engine.py      # extract / score / compose
├── references/
│   ├── scoring-rubric.md
│   └── source-policy.md
└── docs/
    ├── README.en.md
    ├── README.es.md
    └── README.ar.md
```

---

## 4. Instalación y requisitos de entorno

### 4.1 Requisitos base

- Python 3.10+
- Capacidad de búsqueda del agente (Brave / Tavily / Browser)
- Permiso de lectura/escritura en workspace

### 4.2 Comprobación rápida

```bash
python3 scripts/factcheck_engine.py --help
```

Si aparecen `extract|score|compose`, está listo.

---

## 5. CLI opcionales y categorías de cookies (importante)

Estas CLI son **opcionales**. El flujo principal funciona sin ellas.

- CLI de X: <https://github.com/jackwener/twitter-cli>
- CLI de Reddit: <https://github.com/jackwener/rdt-cli>

### 5.1 twitter-cli (modo cookie)

Categorías comunes:

- **Autenticación requerida**: `auth_token`, `ct0`
- **Apoyo de sesión**: `guest_id`, `kdt`
- **Campos opcionales**: `twid`, `lang`

Buenas prácticas:

- Guardar cookies con permisos restringidos.
- Nunca subir cookies a git.
- Rotar cookies de forma periódica.

### 5.2 rdt-cli (modo cookie)

Categorías comunes de cookie/sesión:

- **Sesión principal**: `reddit_session`
- **Dispositivo/seguimiento**: `loid`, `session_tracker`
- **Campos opcionales de autenticación**: `token_v2` (depende de versión)

Buenas prácticas:

- Usar cuenta de mínimo privilegio.
- Renovar cookies expiradas y evitar almacenamiento en texto plano en entornos compartidos.

---

## 6. Flujo de ejecución recomendado

### Paso A: Extraer afirmaciones

```bash
python3 scripts/factcheck_engine.py extract \
  --text "texto de entrada" \
  --output claims.json
```

### Paso B: Verificación en tres rondas (lado agente)

1. **Primero fuentes oficiales/primarias**.
2. **Corroboración independiente en medios principales**.
3. **Búsqueda de contraevidencia/desmentidos**.

Límite recomendado: 6 búsquedas por afirmación. Además, se pueden ejecutar múltiples verificaciones en X(Twitter) (recomendado: 3 rondas) como corroboración social, sin cambiar los conteos de búsquedas oficiales/mainstream/contraevidencia.

### Paso C: Decisión interna

```bash
python3 scripts/factcheck_engine.py score \
  --input evidence.json \
  --output scored.json
```

### Paso D: Componer respuesta al usuario

```bash
python3 scripts/factcheck_engine.py compose \
  --input scored.json \
  --output reply.txt
```

---

## 7. Contrato de campos en evidence.json (detallado)

Campos recomendados por afirmación:

- `claim`
- `type`
- `evidence.official_count`
- `evidence.mainstream_count`
- `evidence.independent_count`
- `evidence.factcheck_true`
- `evidence.factcheck_false`
- `evidence.authority_rebuttal`
- `evidence.outdated_presented_current`
- `evidence.source_chain_hops`
- `evidence.core_contradiction`
- `evidence.has_timestamp`
- `evidence.strong_social_debunk`
- `evidence.out_of_context`
- `evidence.headline_mismatch`
- `evidence.missing_data_citation`
- `evidence.fact_opinion_mixed`

---

## 8. Reglas duras de salida al usuario

La salida al usuario debe ser integrada y **no debe mostrar detalle claim por claim**. Usar siempre esta estructura de 4 partes:

1. **¿Es correcto? (respuesta corta)**: exactamente uno de `correcto | incorrecto | parcialmente correcto | evidencia insuficiente`, más una frase breve.
2. **Situación real**: explicación integrada del estado real del tema.
3. **Conclusión**: juicio final accionable, con nota de incertidumbre si aplica.
4. **Enlaces relacionados (máx. 5)**: hasta 5 enlaces, priorizados como oficial/primario > medios principales confiables > corroboración suplementaria.

Además:
- Nunca mostrar puntuación interna.
- Nunca exponer la lógica interna de puntuación.
- Añadir siempre:

`⚠️ Esta verificación se basa en información públicamente disponible y no puede cubrir materiales privados o de pago.`

---

## 9. Manejo de casos límite

- **Prediction**: sin veredicto verdadero/falso; resumir pronósticos disponibles.
- **Opinion**: marcar como subjetivo y fuera de alcance de fact-check.
- **Satire**: marcar como fuente satírica/ficción.
- **Evidencia insuficiente**: responder “actualmente no verificable” de forma conservadora.

---

## 10. Riesgos y límites

1. La información pública nunca es completa.
2. Las noticias en desarrollo pueden cambiar rápidamente.
3. Las señales sociales son auxiliares, no evidencia principal.
4. Incluso fuentes oficiales pueden tener sesgo institucional; se requiere validación cruzada.

---

## 11. Documentación multilingüe

- Chino: `../README.md`
- Inglés: `README.en.md`
- Árabe: `README.ar.md`



## 12. Prioridad de búsqueda y fallback (v1.0.5)

- Forzar Tavily primero cuando `TAVILY_API_KEY` exista y el servicio esté disponible.
- Usar búsqueda por defecto solo con clave ausente, 401/403, 429/sin cuota o timeouts repetidos.
- El fallback no debe detener el flujo; marcar esas rondas como fallback.

### Mezcla de fuentes
- Tavily/búsqueda general: 50%
- Reddit CLI: 10%
- Twitter CLI: 40%

### Reasignación si falta CLI
- Sin Reddit: +7% Tavily y +3% verificación cruzada de credibilidad.
- Sin Twitter: +28% Tavily y +12% verificación cruzada de credibilidad.
- Sin Reddit y sin Twitter: Tavily 85% + verificación cruzada 15%.

### Aumento de presupuesto de búsqueda
- Ambos CLI disponibles: 10 búsquedas
- Falta 1 CLI: 12 búsquedas
- Faltan 2 CLI: 14 búsquedas

### Llamadas mínimas (base de 10 consultas)
- Tavily: al menos 5 llamadas
- Twitter CLI: al menos 4 llamadas
- Reddit CLI: al menos 1 llamada

> Regla: los mínimos son obligatorios, no uso simbólico de una sola llamada. Si un CLI no está disponible, sus mínimos deben reasignarse a consultas extra de Tavily + verificación cruzada de credibilidad según las reglas de fallback existentes.

## 13. Claim Core First (evitar errores de enfoque)

Priorizar la verdad del reclamo central por encima de detalles periféricos.

1. Capa central (máximo peso): evento/entidad/dirección principal.
2. Capa condicional (peso medio): tiempo/lugar/objeto solo si cambia la verdad.
3. Capa de expresión (peso bajo): tono como “última hora” no debe cambiar el veredicto por sí solo.



## 14. Calibración de severidad (evitar veredictos excesivamente duros)

- Política central: **tolerante con el hecho núcleo, estricta con el error realmente engañoso**.
- Orden de decisión: primero el impacto de desinformación para el usuario, luego la perfección técnica.

### Decisión en cuatro niveles
- **correcto**: el hecho central es verdadero y no hay desvíos materiales en condiciones clave.
- **parcialmente correcto**: el hecho central es verdadero pero hay fallas de contexto/tiempo/redacción.
- **incorrecto**: el hecho central es falso, o errores en condiciones clave cambian la conclusión.
- **evidencia insuficiente**: la evidencia pública no permite confirmar ni refutar el núcleo.

### Reglas anti-severidad excesiva
- Fallas no nucleares (tono de “última hora”, intensidad del titular, desfase temporal no crítico) no deben por sí solas activar `incorrecto`.
- Si el núcleo es verdadero, usar por defecto `parcialmente correcto`, salvo que condiciones clave inviertan la conclusión.



## 15. Puntuación, revisión y política de flexibilidad (ajuste continuo)

- Añadir capa de riesgo de desinformación: alto / medio / bajo.
- Priorizar `parcialmente correcto` salvo que falle el núcleo o que el error en condiciones clave cambie decisiones del usuario.

### Revisión de reversión
- Si `incorrecto` se debe sobre todo al tono de “última hora”, intensidad del titular o desfase temporal no crítico, ejecutar segunda revisión.
- Si no cambia la conclusión/acción, bajar a `parcialmente correcto`.

### Lista no flexible (mantener estricto)
- Seguridad pública
- Riesgo médico y recomendaciones de salud
- Finanzas/fraude
- Fecha de vigencia y aplicabilidad de políticas/regulaciones oficiales
