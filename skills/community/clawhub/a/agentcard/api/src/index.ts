import { appLogger } from "./utils/logger";
import "dotenv/config";
import { createApp } from "./app";
import { env } from "./config/env";

(async () => {
  const app = await createApp();

  app.listen(env.PORT, () => {
    appLogger.info(`ASG Card API listening on http://localhost:${env.PORT}`);
  });
})();
