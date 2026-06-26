# Superpowers — Desarrollo estructurado con sub-agentes

Adaptado de [obra/superpowers](https://github.com/obra/superpowers) para OpenClaw.

## Cuándo activar

Cuando Chema o Luis pidan una **feature nueva, refactor grande, o cambio multi-archivo** en cualquier proyecto (Elicita, FlightCBT, etc.). NO para fixes de una línea o cambios cosméticos.

## El flujo

```
1. BRAINSTORM → 2. PLAN → 3. EXECUTE → 4. REVIEW → 5. SHIP
```

---

## 1. BRAINSTORM (obligatorio)

**HARD GATE: NO escribir código hasta tener diseño aprobado.**

Incluso si parece simple. "Simple" es donde las asunciones matan.

### Pasos:
1. **Explorar contexto** — leer archivos relevantes, commits recientes, estado actual
2. **Preguntar** — UNA pregunta a la vez, preferir opciones múltiples
3. **Proponer 2-3 enfoques** — con trade-offs y tu recomendación
4. **Presentar diseño** — en secciones digeribles, esperar OK antes de avanzar
5. **Guardar diseño** — `docs/plans/YYYY-MM-DD-<feature>-design.md`

### Qué cubrir:
- Arquitectura / componentes afectados
- Flujo de datos
- Manejo de errores
- Cómo se testea
- Impacto en lo existente

---

## 2. PLAN

Después del diseño aprobado, escribir plan de implementación.

### Reglas del plan:
- Guardar en `docs/plans/YYYY-MM-DD-<feature>-plan.md`
- Cada tarea = **2-5 minutos** de trabajo
- **Paths exactos** de archivos a crear/modificar
- **Código completo** en el plan (no "añadir validación")
- **Comandos exactos** con output esperado
- DRY, YAGNI, commits frecuentes

### Estructura de tarea:

```markdown
### Tarea N: [Nombre]

**Archivos:**
- Crear: `ruta/exacta/archivo.ts`
- Modificar: `ruta/exacta/existente.ts`
- Test: `tests/ruta/test.ts`

**Paso 1:** Escribir test que falle
[código completo del test]

**Paso 2:** Verificar que falla
Ejecutar: `npm test -- --grep "nombre"`
Esperado: FAIL

**Paso 3:** Implementación mínima
[código completo]

**Paso 4:** Verificar que pasa
Ejecutar: `npm test -- --grep "nombre"`
Esperado: PASS

**Paso 5:** Commit
`git add ... && git commit -m "feat: descripción"`
```

### Al terminar el plan, preguntar:
> "Plan guardado en `docs/plans/...`. ¿Ejecuto con sub-agentes o prefieres revisarlo primero?"

---

## 3. EXECUTE — Sub-agente por tarea

Un `sessions_spawn` por tarea del plan. Sub-agente fresco = sin contaminación de contexto.

### Prompt del sub-agente implementador:

```
Eres un implementador. Tu ÚNICA tarea es ejecutar exactamente lo que dice el plan.

REGLAS:
- Sigue el plan al pie de la letra
- Si algo no está claro, PARA y pregunta (no improvises)
- Test primero, implementación después
- Commit al terminar
- NO hagas nada que no esté en el plan

TAREA:
[texto completo de la tarea del plan]

CONTEXTO DEL PROYECTO:
[archivos relevantes, stack, convenciones]
```

### Después de cada tarea — doble review:

**Review 1: Spec compliance** (¿hace lo que dice el plan?)
- ¿Se crearon/modificaron los archivos correctos?
- ¿Los tests pasan?
- ¿Se añadió algo que NO estaba en el plan? → revertir
- ¿Falta algo del plan? → completar

**Review 2: Calidad** (¿está bien hecho?)
- ¿El código es limpio?
- ¿Los tests cubren edge cases?
- ¿Hay code smells?

### Si falla un review:
- Lanzar nuevo sub-agente con el feedback específico
- Re-review hasta que pase ambos

---

## 4. REVIEW FINAL

Después de todas las tareas:
- Verificar que el build pasa
- Screenshot de verificación (si hay UI)
- Review completo del diff total
- Documentar en daily notes

---

## 5. SHIP

- `git push`
- Restart PM2 si aplica
- Notificar a Chema con resumen

---

## Principios

- **YAGNI** — No construir lo que no se ha pedido
- **DRY** — No repetir código ni lógica
- **TDD** — Test primero, siempre
- **Fresh context** — Sub-agente nuevo por tarea
- **Evidence over claims** — Verificar antes de declarar victoria
- **El plan es ley** — Si hay que desviarse, parar y re-planificar

---

## Para Elicita específicamente

- **CERO datos demo/ficticios** — regla absoluta
- **Build + PM2 restart + screenshot** después de cada tarea con UI
- **Modelo sub-agentes:** anthropic/claude-sonnet-4-6
- Si algo rompe el build: `git checkout` y documentar
