import type { FastifyInstance } from "fastify";

const CLAWHUB_RAW_BASE =
  "https://raw.githubusercontent.com/openclaw/skills/main";

export async function skillRoutes(app: FastifyInstance) {
  app.get<{ Params: { slug: string } }>(
    "/api/v1/skills/:slug",
    async (request, reply) => {
      const { slug } = request.params;

      const urls = [
        `${CLAWHUB_RAW_BASE}/${slug}/SKILL.md`,
        `https://clawhub.com/api/v1/skills/${slug}/raw`,
      ];

      for (const url of urls) {
        try {
          const res = await fetch(url, {
            signal: AbortSignal.timeout(10000),
            headers: { Accept: "text/plain" },
          });

          if (res.ok) {
            const content = await res.text();
            return reply.send({ slug, content, source: url });
          }
        } catch {
          // try next source
        }
      }

      return reply.status(404).send({
        error: `Skill "${slug}" not found on ClawHub`,
      });
    }
  );

  app.get<{ Params: { slug: string } }>(
    "/api/v1/skills/:slug/scan",
    async (request, reply) => {
      const { slug } = request.params;

      const skillRes = await app.inject({
        method: "GET",
        url: `/api/v1/skills/${slug}`,
      });

      if (skillRes.statusCode !== 200) {
        return reply
          .status(skillRes.statusCode)
          .send(JSON.parse(skillRes.payload));
      }

      const { content } = JSON.parse(skillRes.payload);

      const scanRes = await app.inject({
        method: "POST",
        url: "/api/v1/scans",
        payload: { content, skillName: slug },
      });

      return reply
        .status(scanRes.statusCode)
        .send(JSON.parse(scanRes.payload));
    }
  );
}
