# Juhe Provider Notes

Provider: Juhe flight query API

- Docs: `https://www.juhe.cn/docs/api/id/818`
- Endpoint: `https://apis.juhe.cn/flight/query`
- Required params: `key`, `departure`, `arrival`, `departureDate`
- Optional params used here: `flightNo`, `maxSegments`
- Users must apply for their own Juhe API key and set `JUHE_FLIGHT_API_KEY` or `JUHE_API_KEY`

Known response fields used by this skill:

- `result.orderid`: provider reference ID
- `result.flightInfo[]`
- `flightInfo[].airlineName`
- `flightInfo[].flightNo`
- `flightInfo[].departureName`
- `flightInfo[].departureDate`
- `flightInfo[].departureTime`
- `flightInfo[].arrivalName`
- `flightInfo[].arrivalDate`
- `flightInfo[].arrivalTime`
- `flightInfo[].duration`
- `flightInfo[].ticketPrice`

Important limits:

- `ticketPrice` is a provider reference price, not a booking guarantee.
- Data freshness and fare rules are controlled by Juhe, not by the local script.
- The script is optimized for one-way domestic queries.
- A valid API key must be present in `JUHE_FLIGHT_API_KEY` or `JUHE_API_KEY`.
