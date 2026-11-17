# 05 · Centro de control (`/admin`)

Es la pantalla desde donde manejas tu app sin tocar código ni el panel de Supabase.

## Qué trae la plantilla (`plantillas/app/admin/`)

| Bloque | Para qué |
|---|---|
| **Con acceso** | Cuántas personas pueden entrar hoy. |
| **Lista refrescada** | Cuándo se actualizó la lista por última vez. **Se pone en naranja si pasó más de un día**: es el recordatorio para subir el CSV cuando tu plataforma no tiene API (Skool). |
| **Refrescar la lista** | Subes el CSV → te muestra **+nuevos / −quitados** (con la lista de quitados) → aplicas. Si quita a más del 30%, pide una segunda confirmación. |
| **Un correo suelto** | Dar o quitar acceso a una persona. Estas altas se quedan aunque subas otro CSV. |
| **Quién intentó entrar y no pudo** | Rebotes agrupados por correo. Si un correo rebota 3 veces, es alguien que pagó con otro correo. |
| **Historial** | Cada cambio: cuándo, desde dónde (csv, manual, webhook, pasarela, cron), cuántos entraron y cuántos salieron. |

## Seguridad

- `soloAdmin()` se llama **al inicio de cada página y de cada ruta** de `/admin`. Esconder el botón no es seguridad: cualquiera puede escribir la URL.
- Quién es admin lo decide `ADMIN_EMAILS` en Vercel (separados por coma). Si te equivocas al escribir tu correo ahí, te quedas afuera: se arregla editando la variable y volviendo a desplegar.

## Rutina de 2 minutos (cuando tu plataforma no tiene API)

1. Entra a tu plataforma → Miembros → **Exportar** (CSV).
2. Tu app → `/admin` → Refrescar la lista → elige el archivo → **Ver qué cambia**.
3. Lee los quitados. ¿Tienen sentido? → **Aplicar cambios**.

Hazlo el mismo día de la semana, o todos los días si tu comunidad se mueve mucho. Las altas llegan solas por Zapier. Lo único que hace el CSV es sacar a quien se fue.

## Ideas para agregar después (solo si las vas a usar)

- Buscar a una persona y ver todo lo suyo en una ficha (acceso, pagos, uso).
- Uso de la IA por día y costo **estimado** (rotúlalo como estimado si no mides tokens reales).
- Reenviar el correo de bienvenida.

Regla: cada número del panel tiene que salir de un dato real de la base. Si no existe el dato, el número no se muestra.
