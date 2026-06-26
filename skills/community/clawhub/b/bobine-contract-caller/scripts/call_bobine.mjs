import { execute, signEd25519Call } from "./lib/bobine.mjs"
import { CALL_USAGE, parseOptions, usageAndExit } from "./lib/cli.mjs"
import { parseParams } from "./lib/params.mjs"

const options = parseOptions(process.argv.slice(2))

if (!options.server || !options.module || !options.method) {
  usageAndExit("Missing required call arguments", CALL_USAGE)
}

if (options["auth-module"] && (!options.sigkey || !options.pubkey)) {
  usageAndExit(
    "Signed calls require --auth-module, --sigkey, and --pubkey together",
    CALL_USAGE,
  )
}

try {
  const params = parseParams(options.params)
  const callOptions = {
    server: options.server,
    sparkHex: options["spark-hex"],
    sparkEffort: options["spark-effort"],
  }

  const result = options["auth-module"]
    ? await signEd25519Call(
        options["auth-module"],
        options.module,
        options.method,
        params,
        options.sigkey,
        options.pubkey,
        callOptions,
      )
    : await execute(options.module, options.method, params, callOptions)

  console.log(JSON.stringify(result, null, 2))
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error))
  process.exit(1)
}
