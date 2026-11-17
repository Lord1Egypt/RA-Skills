# 01 · Base de datos (Supabase)

La base de datos es el cuaderno donde tu app anota cosas que tienen que seguir ahí mañana: quién tiene acceso, qué guardó cada persona, qué compró.

## Qué hace Claude y qué haces tú

| Paso | Quién | Cómo |
|---|---|---|
| Crear la cuenta en supabase.com | **Tú** | "Start your project" → entra con GitHub (así no hay otra contraseña que recordar). |
| Crear el proyecto | **Tú** (1 min) | "New project" → nombre = el de tu app · **Region** = la más cercana a tu público (São Paulo para LatAm, Virginia para EE. UU./México, Frankfurt para España) · contraseña de la base: toca "Generate" y **guárdala en tu gestor de contraseñas**, no la vas a volver a ver. |
| Crear tablas, candados, funciones | **Claude** | Con el MCP de Supabase (abajo) o dándote el SQL para pegar en **SQL Editor → Run**. |
| Copiar las llaves a la app | **Tú pegas, Claude guarda** | Ver "Las 3 llaves". |

## Conectar Claude a tu Supabase (opcional, recomendado)

Con el MCP oficial Claude crea las tablas y corre el SQL él mismo, y tú no tienes que copiar ni pegar SQL.

```bash
claude mcp add --transport http supabase "https://mcp.supabase.com/mcp?project_ref=TU_PROJECT_REF"
```

- `TU_PROJECT_REF` es el pedazo de la URL del panel: `supabase.com/dashboard/project/`**`abcdxyz`**.
- La primera vez abre el navegador para que autorices. Después reinicia Claude Code.
- Fijar `project_ref` evita que Claude toque OTRO proyecto tuyo por error.
- Lo que **no** hace: darte la llave `service_role`. Esa la copias tú (es a propósito).
- Supabase advierte que no lo conectes a una base de producción con datos reales sin límites. Mientras construyes está bien. Cuando la app ya tenga gente, agrega `&read_only=true`.

Sin MCP: Claude te da el archivo `.sql` y tú lo pegas en **SQL Editor → New query → Run**. Lo mismo, con un paso más.

## Las 3 llaves (y dónde vive cada una)

Panel → **Project Settings → API Keys** (en proyectos viejos: **Settings → API**).

| Variable | Qué es | ¿Puede verla el navegador? |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | La dirección de tu base | Sí |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Llave pública (en proyectos nuevos se llama **publishable**, empieza con `sb_publishable_`) | Sí |
| `SUPABASE_SERVICE_ROLE_KEY` | **Llave maestra** (en proyectos nuevos, **secret**, empieza con `sb_secret_`). Salta todos los candados. | **NUNCA** |

Reglas que Claude aplica sin negociar:
1. La llave maestra **nunca** lleva `NEXT_PUBLIC_` delante. Con ese prefijo Next.js la mete en el código que baja cualquier visitante.
2. **Nunca** se usa en un archivo que empiece con `'use client'`.
3. Va en `.env.local` (en tu compu) y en Vercel → Settings → Environment Variables. Antes del primer commit, `.env*` tiene que estar en `.gitignore`. Claude lo revisa con `git check-ignore .env.local`.
4. Si alguna vez se sube a GitHub: **rótala en el panel** (botón de regenerar) en ese mismo momento. Borrar el commit no alcanza, porque ya quedó copiada.

## El candado (RLS): la trampa de la lista vacía

Cada tabla nueva se crea con **RLS encendido**. RLS significa que nadie lee nada, a menos que una regla (policy) lo permita.

- **Tablas que solo toca el servidor** (lista de acceso, pagos, historial): RLS encendido y **sin políticas**. Tu servidor usa la llave maestra y pasa igual. Desde el navegador no se ve nada. Así queda el portero.
- **Tablas de la persona** (sus notas, sus guardados): RLS encendido + política `auth.uid() = user_id`, para que cada quien vea solo lo suyo.

⚠️ **La trampa:** si consultas desde el navegador una tabla con RLS y sin políticas, Supabase **no da error**. Devuelve una lista vacía, y parece que "no hay datos". Cuando algo "sale vacío", lo primero que revisa Claude es desde dónde se está leyendo.

Claude corre **Advisors → Security** (o `get_advisors` por MCP) antes de publicar: avisa si quedó alguna tabla sin candado.

## Plan gratis: lo que tienes que saber

- Si pasa **una semana sin actividad**, el proyecto se **pausa** y la app deja de funcionar hasta que lo reactives desde el panel. Una app con uso diario no se pausa. Una app de prueba abandonada sí.
- Cada consulta devuelve **máximo 1000 filas** por defecto. Si tu lista tiene más, hay que paginar (la plantilla `leerLista()` ya lo hace). Si no se pagina, con 1.200 miembros la comparación "quita" a 200 que siguen pagando.

## Verificación antes de seguir

- [ ] `.env.local` tiene las 3 variables y está ignorado por git.
- [ ] Claude hizo una consulta real desde el servidor (por ejemplo, contar filas) y respondió sin error.
- [ ] Advisors → Security sin alertas rojas.
