import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { homedir } from 'node:os'
import { createComputerUseMcpServer } from './vendor/computer-use-mcp/mcpServer.js'
import { buildComputerUseTools } from './vendor/computer-use-mcp/tools.js'
import { filterAppsForDescription } from './computer-use/appNames.js'
import { getComputerUseHostAdapter } from './computer-use/hostAdapter.js'
import { getChicagoCoordinateMode } from './computer-use/gates.js'
import { createSessionContext } from './session.js'
import { logDebug } from './lib/log.js'

async function getInstalledAppNames(): Promise<string[] | undefined> {
  try {
    const installed = await getComputerUseHostAdapter().executor.listInstalledApps()
    return filterAppsForDescription(installed, homedir())
  } catch {
    return undefined
  }
}

export async function runServer(): Promise<void> {
  const adapter = getComputerUseHostAdapter()
  const coordinateMode = getChicagoCoordinateMode()
  const context = createSessionContext()
  const server = createComputerUseMcpServer(adapter, coordinateMode, context)
  const installedAppNames = await getInstalledAppNames()
  const tools = buildComputerUseTools(adapter.executor.capabilities, coordinateMode, installedAppNames)
  server.setRequestHandler((await import('@modelcontextprotocol/sdk/types.js')).ListToolsRequestSchema, async () =>
    adapter.isDisabled() ? { tools: [] } : { tools },
  )
  const transport = new StdioServerTransport()
  logDebug('starting stdio MCP server')
  await server.connect(transport)
}
