export default {

  async get_doctores(_params, { config }) {
    return apiFetch(`${config.baseUrl}/api/doctores.php`, 'GET', null, config.apiKey);
  },

  async get_turnos_disponibles({ doctor_id, fecha }, { config }) {
    if (!doctor_id || !fecha) {
      return { error: true, message: 'Se requieren doctor_id y fecha (YYYY-MM-DD)' };
    }
    const qs = new URLSearchParams({ doctor_id, fecha });
    return apiFetch(`${config.baseUrl}/api/turnos_disponibles.php?${qs}`, 'GET', null, config.apiKey);
  },

  async buscar_paciente({ documento }, { config }) {
    if (!documento) {
      return { error: true, message: 'Se requiere el campo documento' };
    }
    const qs = new URLSearchParams({ documento });
    return apiFetch(`${config.baseUrl}/api/buscar_paciente.php?${qs}`, 'GET', null, config.apiKey);
  },

  async agendar_turno({ paciente_id, doctor_id, fecha, hora, motivo }, { config }) {
    const faltantes = ['paciente_id', 'doctor_id', 'fecha', 'hora', 'motivo']
      .filter(campo => !arguments[0][campo]);

    if (faltantes.length > 0) {
      return { error: true, message: `Campos requeridos faltantes: ${faltantes.join(', ')}` };
    }

    return apiFetch(
      `${config.baseUrl}/api/agendar_turno.php`,
      'POST',
      { paciente_id, doctor_id, fecha, hora, motivo },
      config.apiKey
    );
  },
};

// ─── Utilidad HTTP ────────────────────────────────────────────────────────────

async function apiFetch(url, method, body, token) {
  const opciones = {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type':  'application/json',
      'Accept':        'application/json',
    },
  };

  if (body && ['POST', 'PUT', 'PATCH'].includes(method)) {
    opciones.body = JSON.stringify(body);
  }

  let res;
  try {
    res = await fetch(url, opciones);
  } catch (err) {
    return { error: true, message: `Error de red: ${err.message}` };
  }

  const texto = await res.text();
  let datos;

  try {
    datos = JSON.parse(texto);
  } catch {
    return { error: true, status: res.status, message: texto.slice(0, 500) };
  }

  if (!res.ok) {
    return { error: true, status: res.status, ...datos };
  }

  return datos;
}
