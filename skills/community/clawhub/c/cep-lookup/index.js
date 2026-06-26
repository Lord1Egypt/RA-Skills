const axios = require('axios');

module.exports = async function(context) {
    const message = context.message.text;

    // Supports: "cep 01001-000", "CEP 01001000" and "details for CEP 01001-000"
    const match = message.match(/cep[:\s]+(\d{5}-?\d{3})/i);

    if (!match) {
        return "Invalid CEP format. Try something like: cep 01001-000";
    }

    const cep = match[1].replace("-", "");

    try {
        const response = await axios.get(`https://viacep.com.br/ws/${cep}/json/`);
        const data = response.data;

        if (data.erro) {
            return `CEP ${cep} not found.`;
        }

        return `Details for CEP ${cep}:
- Street: ${data.logradouro}
- Neighborhood: ${data.bairro}
- City: ${data.localidade}
- State: ${data.uf}
- Complement: ${data.complemento || "none"}`;

    } catch (err) {
        console.error(err);
        return "Error looking up CEP. Please try again later.";
    }
};
