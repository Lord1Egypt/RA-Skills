# CEP Lookup Skill for OpenClaw 📮

This OpenClaw skill allows users to look up Brazilian postal codes (CEP) quickly and easily using the [ViaCEP API](https://viacep.com.br).  
It returns detailed address information including **street (logradouro), neighborhood (bairro), city (localidade), state (uf), and complement**.

---

## Features

- Query any valid Brazilian CEP.
- Returns complete address information.
- Easy to install and use with OpenClaw.
- No API key required – uses the public ViaCEP service.

---

## Installation

1. Copy the folder to the OpenClaw skills directory:

```bash
cp -r cepSkill ~/.openclaw/workspace/skills/

cd ~/.openclaw/workspace/skills/cepSkill
npm install
```

---

## Usage

Once installed, you can use the skill by simply asking:

```
cep 01001-000
```

or

```
What are the details for CEP 20040-020
```

The skill will return a message like:

```
Details for CEP 01001000:
- Street: Praça da Sé
- Neighborhood: Sé
- City: São Paulo
- State: SP
- Complement: none
```

## Example Queries

```
cep 30140-110
What are the details for CEP 20040-020
```

## Notes

- The skill only works with valid Brazilian CEPs.
- Ensure your OpenClaw instance has internet access to reach the ViaCEP API.
- No authentication is required to use the ViaCEP service.
- The trigger pattern supports both Portuguese (`cep XXXXX-XXX`) and English (`details for CEP XXXXX-XXX`).

## Dependencies

- [axios](https://www.npmjs.com/package/axios) – for HTTP requests.

Install dependencies with:

```bash
npm install
```

## Contributing

Feel free to fork the repository, improve the skill, or add additional features for Brazilian address lookup.

## License

MIT License
