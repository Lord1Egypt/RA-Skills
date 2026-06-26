---
name: clawhub-skill-creator
description: Create and publish ClawHub skills with the correct format. Includes YAML frontmatter template, _meta.json structure, and step-by-step publishing guide.
---

# ClawHub Skill Creator

Este skill proporciona instrucciones completas para **crear y publicar skills en ClawHub** con el formato correcto desde el primer intento.

---

## 🎯 **Cuándo Usar Este Skill**

Usa este skill cuando el usuario quiera:

- Crear un skill nuevo para ClawHub
- Publicar un skill existente en ClawHub
- Corregir el formato de un skill mal estructurado
- Aprender la estructura correcta de un skill
- Entender el proceso de publicación paso a paso

---

## 📁 **Estructura de Archivos Requerida**

Un skill de ClawHub debe tener esta estructura mínima:

```
nombre-del-skill/
├── SKILL.md          # Obligatorio - Documentación del skill
└── _meta.json        # Obligatorio - Metadatos del skill
```

**Archivos opcionales:**
```
nombre-del-skill/
├── README.md         # Documentación adicional
├── scripts/          # Scripts ejecutables
├── references/       # Referencias y ejemplos
└── assets/           # Recursos adicionales
```

---

## 📝 **Formato Correcto de SKILL.md**

### **YAML Frontmatter (OBLIGATORIO)**

El archivo `SKILL.md` **DEBE** comenzar con YAML frontmatter en este formato exacto:

```yaml
---
name: nombre-del-skill
description: Descripción clara y concisa del skill (máx 160 caracteres)
---
```

**Campos requeridos:**
- `name`: Nombre del skill (kebab-case, sin espacios, minúsculas)
- `description`: Descripción breve (aparece en ClawHub search)

**Ejemplo real:**
```yaml
---
name: lossless-claw-skill
description: Wrapper seguro para el plugin lossless-claw (LCM). Proporciona interfaz para lcm_grep, lcm_describe, lcm_expand_query.
---
```

### **Contenido del SKILL.md**

Después del frontmatter, incluye:

```markdown
# Nombre del Skill

Descripción extendida del propósito del skill.

---

## Descripción

Explicación detallada de qué hace el skill y por qué es útil.

## Cuándo Usar Este Skill

Lista de casos de uso específicos:

- Cuando el usuario necesita X
- Cuando ocurre Y
- Para resolver Z

## Cómo Usar

Instrucciones paso a paso o ejemplos de comandos.

## Ejemplos

```bash
npx clawhub install nombre-del-skill
```

## Notas Adicionales

Información extra, advertencias, o referencias.
```

---

## 📋 **Formato de _meta.json**

El archivo `_meta.json` debe tener esta estructura:

```json
{
  "name": "nombre-del-skill",
  "description": "Descripción clara y concisa del skill",
  "version": "1.0.0",
  "tags": ["categoria", "utilidad", "feature"]
}
```

**Campos requeridos:**
- `name`: Mismo nombre que en el YAML frontmatter
- `description`: Misma descripción que en el YAML frontmatter
- `version`: Versión semántica (recomendado: "1.0.0" para inicio)
- `tags`: Array de tags para búsqueda (mínimo 1, máximo 5)

**Ejemplo real:**
```json
{
  "name": "lossless-claw-skill",
  "description": "Wrapper seguro para el plugin lossless-claw (LCM). Proporciona interfaz para lcm_grep, lcm_describe, lcm_expand_query.",
  "version": "1.0.0",
  "tags": ["latest", "lcm", "memory", "context"]
}
```

---

## 🚀 **Proceso de Publicación Paso a Paso**

### **Paso 1: Preparar el Skill**

```bash
# 1. Crear directorio
mkdir -p /ruta/a/skills/nombre-del-skill

# 2. Crear SKILL.md con YAML frontmatter correcto
# 3. Crear _meta.json con estructura válida
```

### **Paso 2: Verificar Formato**

Antes de publicar, verifica:

- [ ] `SKILL.md` tiene YAML frontmatter (`---` al inicio y fin)
- [ ] `name` en YAML coincide con `name` en `_meta.json`
- [ ] `description` en YAML coincide con `description` en `_meta.json`
- [ ] El nombre usa kebab-case (guiones, sin espacios)
- [ ] `_meta.json` es JSON válido (puedes validar en jsonlint.com)

### **Paso 3: Autenticar CLI de ClawHub**

```bash
# Ejecutar comando de login
npx clawhub login

# Se abrirá una URL en el browser:
# https://clawhub.ai/cli/auth?redirect_uri=...

# Navegar a esa URL en el browser
# El proceso CLI esperará el callback automáticamente
```

**Nota:** Debes tener una cuenta de GitHub con **más de 14 días de antigüedad**.

### **Paso 4: Publicar el Skill**

```bash
npx clawhub publish /ruta/completa/al/skill \
  --slug nombre-del-skill \
  --name "Nombre Display del Skill" \
  --version 1.0.0 \
  --tags "tag1,tag2,tag3"
```

**Ejemplo real:**
```bash
npx clawhub publish /mnt/data/openclaw/workspace/.openclaw/workspace/skills/lossless-claw-skill \
  --slug lossless-claw-skill \
  --name "Lossless Claw Skill" \
  --version 1.0.0 \
  --tags "latest,lcm,memory,context"
```

### **Paso 5: Verificar Publicación**

Después de publicar, verás un mensaje como:

```
✔ OK. Published nombre-del-skill@1.0.0 (k97b6tvrydfc8ez4z02h8aamc9840cg2)
```

**URL del skill:**
```
https://clawhub.ai/{ID}/{slug}
Ejemplo: https://clawhub.ai/k97b6tvrydfc8ez4z02h8aamc9840cg2/lossless-claw-skill
```

---

## ⚠️ **Errores Comunes y Soluciones**

### **Error 1: "Path must be a folder"**

**Causa:** La ruta no es absoluta o la carpeta no existe.

**Solución:**
```bash
# Usar ruta absoluta completa
npx clawhub publish /mnt/data/openclaw/workspace/.openclaw/workspace/skills/nombre-del-skill
```

### **Error 2: "Not logged in. Run: clawhub login"**

**Causa:** La CLI no está autenticada.

**Solución:**
```bash
npx clawhub login
# Navegar a la URL que aparece en el output
```

### **Error 3: "GitHub API rate limit exceeded"**

**Causa:** Límite temporal de API de GitHub.

**Solución:** Esperar 30-60 segundos y reintentar.

### **Error 4: "GitHub account must be at least 14 days old"**

**Causa:** La cuenta de GitHub fue creada recientemente.

**Solución:** Usar una cuenta de GitHub con más de 14 días de antigüedad.

### **Error 5: Skill no aparece en ClawHub panel después de instalar**

**Causa:** Formato incorrecto de YAML frontmatter.

**Solución:** Verificar que el frontmatter sea exactamente:
```yaml
---
name: nombre-del-skill
description: Descripción del skill
---
```

**NO usar este formato incorrecto:**
```yaml
# ❌ INCORRECTO - Muy complejo
name: skill-name
description: ...
author: ...
version: ...
```

---

## 📚 **Ejemplos de Skills Reales**

### **Ejemplo 1: Skill Simple (Wrapper)**

**SKILL.md:**
```yaml
---
name: lossless-claw-skill
description: Wrapper seguro para el plugin lossless-claw (LCM).
---

# Lossless Claw Skill

Skill wrapper para el plugin lossless-claw de OpenClaw.

## Descripción

Proporciona una interfaz segura para las herramientas LCM.

## Cuándo Usar

- Cuando necesitas buscar en el historial de conversación
- Cuando necesitas expandir resúmenes compactados
- Para queries complejas de memoria
```

**_meta.json:**
```json
{
  "name": "lossless-claw-skill",
  "description": "Wrapper seguro para el plugin lossless-claw (LCM).",
  "version": "1.0.0",
  "tags": ["latest", "lcm", "memory"]
}
```

### **Ejemplo 2: Skill con Scripts**

**SKILL.md:**
```yaml
---
name: weather-skill
description: Obtén el clima actual y pronósticos vía wttr.in o Open-Meteo.
---

# Weather Skill

Obtén información meteorológica para cualquier ubicación.

## Cuándo Usar

- Cuando el usuario pregunta sobre el clima
- Para pronósticos de 1-7 días
- Para temperaturas actuales

## Comandos

```bash
curl wttr.in/Ciudad
```
```

**_meta.json:**
```json
{
  "name": "weather-skill",
  "description": "Obtén el clima actual y pronósticos vía wttr.in o Open-Meteo.",
  "version": "1.0.0",
  "tags": ["weather", "forecast", "utility"]
}
```

---

## 🎓 **Checklist de Publicación**

Antes de publicar, verifica:

- [ ] **Estructura de archivos**
  - [ ] `SKILL.md` existe
  - [ ] `_meta.json` existe
  - [ ] Ambos están en la misma carpeta

- [ ] **YAML Frontmatter**
  - [ ] Comienza con `---`
  - [ ] Tiene campo `name`
  - [ ] Tiene campo `description`
  - [ ] Termina con `---`
  - [ ] No hay otros campos innecesarios

- [ ] **_meta.json**
  - [ ] Es JSON válido
  - [ ] Tiene campo `name` (mismo que YAML)
  - [ ] Tiene campo `description` (mismo que YAML)
  - [ ] Tiene campo `version`
  - [ ] Tiene campo `tags` (array)

- [ ] **CLI Autenticada**
  - [ ] `npx clawhub login` ejecutado
  - [ ] URL de auth navegada en browser
  - [ ] Mensaje "OK. Logged in as @usuario" apareció

- [ ] **Cuenta GitHub**
  - [ ] Cuenta tiene más de 14 días de antigüedad
  - [ ] No hay rate limit activo (esperar 60s si hay error)

---

## 🔗 **Recursos Adicionales**

- **ClawHub:** https://clawhub.ai
- **Documentación OpenClaw:** https://docs.openclaw.ai
- **Skills existentes:** https://clawhub.ai/skills
- **GitHub:** https://github.com/openclaw/openclaw

---

## 💡 **Consejos Profesionales**

1. **Mantén el frontmatter simple** - Solo `name` y `description` son requeridos
2. **Usa kebab-case** - `nombre-del-skill`, no `NombreDelSkill` ni `nombre_del_skill`
3. **Descripciones claras** - Máximo 160 caracteres, explica qué hace el skill
4. **Tags relevantes** - Usa 3-5 tags que describan la funcionalidad
5. **Versiona correctamente** - Empieza en 1.0.0, usa semver para updates
6. **Prueba localmente** - Verifica que el skill funcione antes de publicar
7. **Documenta bien** - Un SKILL.md claro ayuda a otros a usar tu skill

---

**Creado con ❤️ para la comunidad OpenClaw**
