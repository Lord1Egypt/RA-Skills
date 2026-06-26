# Game Developer — Code Examples

## Example 1

```csharp
// GameCore.cs - Unity Core Game Architecture
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using Unity.Netcode;
using Unity.Collections;
using Unity.Jobs;
using Unity.Burst;
using Unity.Mathematics;

namespace GameFramework
{
    // Game State Management
    public enum GameState
    {
        MainMenu,
        Loading,
        Playing,
        Paused,
        GameOver,
        Victory
    }

    public class GameManager : NetworkBehaviour
    {
        private static GameManager _instance;
        public static GameManager Instance
        {
            get
            {
                if (_instance == null)
                {
                    _instance = FindObjectOfType<GameManager>();
                    if (_instance == null)
                    {
                        GameObject go = new GameObject("GameManager");
                        _instance = go.AddComponent<GameManager>();
                        DontDestroyOnLoad(go);
                    }
                }
                return _instance;
            }
        }

        [Header("Game Configuration")]
        [SerializeField] private GameConfig gameConfig;
        [SerializeField] private GameState currentState = GameState.MainMenu;
        
        [Header("Events")]
        public UnityEvent<GameState> OnGameStateChanged;
        public UnityEvent<int> OnScoreChanged;
        public UnityEvent<float> OnHealthChanged;
        
        private Dictionary<string, object> gameData = new Dictionary<string, object>();
        private SaveSystem saveSystem;
        private InputManager inputManager;
        private AudioManager audioManager;
        private PoolManager poolManager;

        protected override void Awake()
        {
            base.Awake();
            if (_instance != null && _instance != this)
            {
                Destroy(gameObject);
                return;
            }
            _instance = this;
            DontDestroyOnLoad(gameObject);
            
            InitializeSystems();
        }

        private void InitializeSystems()
        {
            saveSystem = new SaveSystem();
            inputManager = GetComponent<InputManager>() ?? gameObject.AddComponent<InputManager>();
            audioManager = GetComponent<AudioManager>() ?? gameObject.AddComponent<AudioManager>();
            poolManager = GetComponent<PoolManager>() ?? gameObject.AddComponent<PoolManager>();
            
            // Initialize networking if needed
            if (gameConfig.isMultiplayer)
            {
                InitializeNetworking();
            }
        }

        private void InitializeNetworking()
        {
            NetworkManager networkManager = GetComponent<NetworkManager>();
            if (networkManager == null)
            {
                networkManager = gameObject.AddComponent<NetworkManager>();
            }
            
            // Configure network settings
            networkManager.NetworkConfig.PlayerPrefab = gameConfig.playerPrefab;
            networkManager.NetworkConfig.NetworkTransport = gameConfig.networkTransport;
        }

        public void ChangeGameState(GameState newState)
        {
            if (currentState == newState) return;
            
            // Exit current state
            ExitState(currentState);
            
            // Enter new state
            currentState = newState;
            EnterState(newState);
            
            // Notify listeners
            OnGameStateChanged?.Invoke(newState);
            
            // Sync state across network
            if (IsServer && gameConfig.isMultiplayer)
            {
                SyncGameStateClientRpc(newState);
            }
        }

        [ClientRpc]
        private void SyncGameStateClientRpc(GameState newState)
        {
            if (!IsServer)
            {
                currentState = newState;
                OnGameStateChanged?.Invoke(newState);
            }
        }

        private void EnterState(GameState state)
        {
            switch (state)
            {
                case GameState.MainMenu:
                    Time.timeScale = 1f;
                    inputManager.SetInputMode(InputMode.Menu);
                    audioManager.PlayMusic("MainMenu");
                    break;
                    
                case GameState.Loading:
                    StartCoroutine(LoadGameResources());
                    break;
                    
                case GameState.Playing:
                    Time.timeScale = 1f;
                    inputManager.SetInputMode(InputMode.Gameplay);
                    audioManager.PlayMusic("Gameplay");
                    break;
                    
                case GameState.Paused:
                    Time.timeScale = 0f;
                    inputManager.SetInputMode(InputMode.Menu);
                    break;
                    
                case GameState.GameOver:
                    Time.timeScale = 0.5f;
                    SaveHighScore();
                    ShowGameOverUI();
                    break;
            }
        }

        private void ExitState(GameState state)
        {
            switch (state)
            {
                case GameState.Paused:
                    Time.timeScale = 1f;
                    break;
            }
        }

        private System.Collections.IEnumerator LoadGameResources()
        {
            float progress = 0f;
            
            // Load essential resources
            yield return LoadResourceAsync("Prefabs", p => progress = p * 0.3f);
            yield return LoadResourceAsync("Materials", p => progress = 0.3f + p * 0.2f);
            yield return LoadResourceAsync("Audio", p => progress = 0.5f + p * 0.2f);
            yield return LoadResourceAsync("UI", p => progress = 0.7f + p * 0.3f);
            
            // Initialize game world
            yield return InitializeGameWorld();
            
            ChangeGameState(GameState.Playing);
        }

        private System.Collections.IEnumerator LoadResourceAsync(string path, Action<float> onProgress)
        {
            var request = Resources.LoadAsync(path);
            while (!request.isDone)
            {
                onProgress?.Invoke(request.progress);
                yield return null;
            }
        }

        private System.Collections.IEnumerator InitializeGameWorld()
        {
            // Spawn environment
            SpawnEnvironment();
            yield return null;
            
            // Spawn players
            if (gameConfig.isMultiplayer)
            {
                SpawnNetworkPlayers();
            }
            else
            {
                SpawnLocalPlayer();
            }
            yield return null;
            
            // Initialize AI
            InitializeAI();
            yield return null;
        }

        private void SaveHighScore()
        {
            int currentScore = (int)gameData.GetValueOrDefault("Score", 0);
            int highScore = PlayerPrefs.GetInt("HighScore", 0);
            
            if (currentScore > highScore)
            {
                PlayerPrefs.SetInt("HighScore", currentScore);
                PlayerPrefs.Save();
            }
        }

        private void ShowGameOverUI()
        {
            // Implementation for game over UI
        }

        private void SpawnEnvironment()
        {
            // Implementation for environment spawning
        }

        private void SpawnNetworkPlayers()
        {
            // Implementation for network player spawning
        }

        private void SpawnLocalPlayer()
        {
            GameObject player = Instantiate(gameConfig.playerPrefab);
            player.transform.position = gameConfig.playerSpawnPoint;
        }

        private void InitializeAI()
        {
            // Implementation for AI initialization
        }
    }

    // Advanced Character Controller
    [RequireComponent(typeof(CharacterController))]
    public class AdvancedCharacterController : NetworkBehaviour
    {
        [Header("Movement Settings")]
        [SerializeField] private float walkSpeed = 5f;
        [SerializeField] private float runSpeed = 10f;
        [SerializeField] private float jumpHeight = 2f;
        [SerializeField] private float gravity = -9.81f;
        [SerializeField] private float airControl = 0.3f;
        
        [Header("Advanced Movement")]
        [SerializeField] private float dashDistance = 5f;
        [SerializeField] private float dashCooldown = 1f;
        [SerializeField] private float wallJumpForce = 7f;
        [SerializeField] private float slideSpeed = 15f;
        [SerializeField] private float climbSpeed = 3f;
        
        [Header("Ground Check")]
        [SerializeField] private Transform groundCheck;
        [SerializeField] private float groundDistance = 0.4f;
        [SerializeField] private LayerMask groundMask;
        
        private CharacterController controller;
        private Vector3 velocity;
        private bool isGrounded;
        private bool isWallRunning;
        private bool isSliding;
        private bool isClimbing;
        private float lastDashTime;
        private Vector3 wallNormal;
        
        // Network variables
        private NetworkVariable<Vector3> networkPosition = new NetworkVariable<Vector3>();
        private NetworkVariable<Quaternion> networkRotation = new NetworkVariable<Quaternion>();
        
        // Input buffer for smoother controls
        private Queue<InputCommand> inputBuffer = new Queue<InputCommand>();
        private const int MaxInputBufferSize = 10;

        private void Awake()
        {
            controller = GetComponent<CharacterController>();
        }

        public override void OnNetworkSpawn()
        {
            if (IsOwner)
            {
                // Setup local player controls
                InputManager.Instance.OnMoveInput += HandleMoveInput;
                InputManager.Instance.OnJumpInput += HandleJumpInput;
                InputManager.Instance.OnDashInput += HandleDashInput;
            }
        }

        private void Update()
        {
            if (!IsOwner && gameConfig.isMultiplayer)
            {
                // Interpolate position for non-owners
                transform.position = Vector3.Lerp(transform.position, networkPosition.Value, Time.deltaTime * 10f);
                transform.rotation = Quaternion.Lerp(transform.rotation, networkRotation.Value, Time.deltaTime * 10f);
                return;
            }
            
            // Ground check
            isGrounded = Physics.CheckSphere(groundCheck.position, groundDistance, groundMask);
            
            // Process input buffer
            ProcessInputBuffer();
            
            // Apply movement
            ApplyMovement();
            
            // Sync position across network
            if (IsOwner && gameConfig.isMultiplayer)
            {
                UpdateNetworkPositionServerRpc(transform.position, transform.rotation);
            }
        }

        private void ProcessInputBuffer()
        {
            while (inputBuffer.Count > 0 && inputBuffer.Count <= MaxInputBufferSize)
            {
                InputCommand command = inputBuffer.Dequeue();
                ExecuteCommand(command);
            }
        }

        private void ExecuteCommand(InputCommand command)
        {
            switch (command.type)
            {
                case InputType.Move:
                    ApplyMovementInput(command.moveDirection);
                    break;
                case InputType.Jump:
                    PerformJump();
                    break;
                case InputType.Dash:
                    PerformDash(command.dashDirection);
                    break;
            }
        }

        private void ApplyMovement()
        {
            // Apply gravity
            if (isGrounded && velocity.y < 0)
            {
                velocity.y = -2f;
            }
            else
            {
                velocity.y += gravity * Time.deltaTime;
            }
            
            // Special movement states
            if (isWallRunning)
            {
                ApplyWallRun();
            }
            else if (isSliding)
            {
                ApplySlide();
            }
            else if (isClimbing)
            {
                ApplyClimb();
            }
            
            // Move character
            controller.Move(velocity * Time.deltaTime);
        }

        private void PerformJump()
        {
            if (isGrounded)
            {
                velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
                audioManager.PlaySFX("Jump");
            }
            else if (isWallRunning)
            {
                // Wall jump
                velocity = wallNormal * wallJumpForce;
                velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
                isWallRunning = false;
                audioManager.PlaySFX("WallJump");
            }
        }

        private void PerformDash(Vector3 direction)
        {
            if (Time.time - lastDashTime < dashCooldown) return;
            
            lastDashTime = Time.time;
            velocity = direction * dashDistance;
            
            // Visual effects
            ParticleSystem dashEffect = poolManager.GetFromPool<ParticleSystem>("DashEffect");
            dashEffect.transform.position = transform.position;
            dashEffect.Play();
            
            audioManager.PlaySFX("Dash");
        }

        private void ApplyWallRun()
        {
            // Wall run physics
            velocity.y = Mathf.Lerp(velocity.y, 0f, Time.deltaTime * 5f);
            
            // Move along wall
            Vector3 wallForward = Vector3.Cross(wallNormal, Vector3.up);
            velocity = wallForward * walkSpeed;
        }

        private void ApplySlide()
        {
            // Slide physics
            velocity = transform.forward * slideSpeed;
            velocity.y = gravity * Time.deltaTime;
        }

        private void ApplyClimb()
        {
            // Climbing physics
            velocity = Vector3.up * climbSpeed;
        }

        [ServerRpc]
        private void UpdateNetworkPositionServerRpc(Vector3 position, Quaternion rotation)
        {
            networkPosition.Value = position;
            networkRotation.Value = rotation;
        }

        private void HandleMoveInput(Vector2 input)
        {
            if (inputBuffer.Count >= MaxInputBufferSize) return;
            
            inputBuffer.Enqueue(new InputCommand
            {
                type = InputType.Move,
                moveDirection = new Vector3(input.x, 0, input.y),
                timestamp = Time.time
            });
        }

        private void HandleJumpInput()
        {
            if (inputBuffer.Count >= MaxInputBufferSize) return;
            
            inputBuffer.Enqueue(new InputCommand
            {
                type = InputType.Jump,
                timestamp = Time.time
            });
        }

        private void HandleDashInput(Vector3 direction)
        {
            if (inputBuffer.Count >= MaxInputBufferSize) return;
            
            inputBuffer.Enqueue(new InputCommand
            {
                type = InputType.Dash,
                dashDirection = direction,
                timestamp = Time.time
            });
        }

        private void ApplyMovementInput(Vector3 moveDirection)
        {
            float currentSpeed = Input.GetKey(KeyCode.LeftShift) ? runSpeed : walkSpeed;
            
            if (isGrounded)
            {
                Vector3 move = transform.right * moveDirection.x + transform.forward * moveDirection.z;
                velocity = move * currentSpeed;
            }
            else
            {
                // Air control
                Vector3 move = transform.right * moveDirection.x + transform.forward * moveDirection.z;
                velocity += move * currentSpeed * airControl * Time.deltaTime;
            }
        }
    }

    // Combat System
    public class CombatSystem : NetworkBehaviour
    {
        [Header("Combat Settings")]
        [SerializeField] private float damage = 10f;
        [SerializeField] private float attackRange = 2f;
        [SerializeField] private float attackCooldown = 0.5f;
        [SerializeField] private LayerMask enemyLayers;
        
        [Header("Combo System")]
        [SerializeField] private ComboAttack[] comboAttacks;
        [SerializeField] private float comboTimeout = 1f;
        
        private Queue<AttackInput> attackBuffer = new Queue<AttackInput>();
        private List<AttackInput> currentCombo = new List<AttackInput>();
        private float lastAttackTime;
        private int comboCounter;
        
        // Network sync
        private NetworkVariable<float> networkHealth = new NetworkVariable<float>(100f);
        
        [System.Serializable]
        public class ComboAttack
        {
            public string name;
            public AttackInput[] sequence;
            public float damageMultiplier;
            public AnimationClip animation;
            public ParticleSystem effect;
            public AudioClip soundEffect;
        }

        private void Update()
        {
            if (!IsOwner) return;
            
            // Check combo timeout
            if (Time.time - lastAttackTime > comboTimeout && currentCombo.Count > 0)
            {
                ResetCombo();
            }
            
            // Process attack buffer
            ProcessAttackBuffer();
        }

        public void PerformAttack(AttackInput input)
        {
            if (Time.time - lastAttackTime < attackCooldown) return;
            
            attackBuffer.Enqueue(input);
            lastAttackTime = Time.time;
        }

        private void ProcessAttackBuffer()
        {
            while (attackBuffer.Count > 0)
            {
                AttackInput input = attackBuffer.Dequeue();
                currentCombo.Add(input);
                
                // Check for combo match
                ComboAttack matchedCombo = CheckComboMatch();
                if (matchedCombo != null)
                {
                    ExecuteCombo(matchedCombo);
                    ResetCombo();
                }
                else if (currentCombo.Count == 1)
                {
                    // Execute basic attack
                    ExecuteBasicAttack(input);
                }
            }
        }

        private ComboAttack CheckComboMatch()
        {
            foreach (var combo in comboAttacks)
            {
                if (MatchesCombo(combo.sequence))
                {
                    return combo;
                }
            }
            return null;
        }

        private bool MatchesCombo(AttackInput[] sequence)
        {
            if (currentCombo.Count != sequence.Length) return false;
            
            for (int i = 0; i < sequence.Length; i++)
            {
                if (currentCombo[i] != sequence[i]) return false;
            }
            
            return true;
        }

        private void ExecuteCombo(ComboAttack combo)
        {
            // Play animation
            GetComponent<Animator>().Play(combo.animation.name);
            
            // Apply damage
            float totalDamage = damage * combo.damageMultiplier;
            ApplyAreaDamage(transform.position, attackRange * 1.5f, totalDamage);
            
            // Visual effects
            if (combo.effect != null)
            {
                Instantiate(combo.effect, transform.position, Quaternion.identity);
            }
            
            // Audio
            if (combo.soundEffect != null)
            {
                audioManager.PlaySFX(combo.soundEffect);
            }
            
            // Network sync
            if (IsServer)
            {
                ExecuteComboClientRpc(combo.name);
            }
        }

        [ClientRpc]
        private void ExecuteComboClientRpc(string comboName)
        {
            // Sync combo execution across clients
            Debug.Log($"Combo executed: {comboName}");
        }

        private void ExecuteBasicAttack(AttackInput input)
        {
            // Perform raycast or overlap check
            Collider[] hitEnemies = Physics.OverlapSphere(transform.position, attackRange, enemyLayers);
            
            foreach (Collider enemy in hitEnemies)
            {
                IDamageable damageable = enemy.GetComponent<IDamageable>();
                if (damageable != null)
                {
                    damageable.TakeDamage(damage, transform.position);
                }
            }
        }

        private void ApplyAreaDamage(Vector3 center, float radius, float damageAmount)
        {
            Collider[] hitEnemies = Physics.OverlapSphere(center, radius, enemyLayers);
            
            foreach (Collider enemy in hitEnemies)
            {
                IDamageable damageable = enemy.GetComponent<IDamageable>();
                if (damageable != null)
                {
                    // Calculate damage falloff based on distance
                    float distance = Vector3.Distance(center, enemy.transform.position);
                    float falloff = 1f - (distance / radius);
                    float finalDamage = damageAmount * falloff;
                    
                    damageable.TakeDamage(finalDamage, center);
                }
            }
        }

        private void ResetCombo()
        {
            currentCombo.Clear();
            comboCounter = 0;
        }

        public void TakeDamage(float amount)
        {
            if (!IsServer) return;
            
            networkHealth.Value = Mathf.Max(0, networkHealth.Value - amount);
            
            if (networkHealth.Value <= 0)
            {
                Die();
            }
        }

        private void Die()
        {
            // Handle death
            GameManager.Instance.ChangeGameState(GameState.GameOver);
        }
    }

    // AI System using Unity Job System
    [BurstCompile]
    public struct AIPathfindingJob : IJobParallelFor
    {
        [ReadOnly] public NativeArray<float3> positions;
        [ReadOnly] public NativeArray<float3> targets;
        [ReadOnly] public float deltaTime;
        [ReadOnly] public float moveSpeed;
        
        public NativeArray<float3> velocities;
        
        public void Execute(int index)
        {
            float3 direction = math.normalize(targets[index] - positions[index]);
            velocities[index] = direction * moveSpeed * deltaTime;
        }
    }

    public class AIManager : MonoBehaviour
    {
        [SerializeField] private int maxAIAgents = 100;
        [SerializeField] private float aiUpdateInterval = 0.1f;
        
        private NativeArray<float3> aiPositions;
        private NativeArray<float3> aiTargets;
        private NativeArray<float3> aiVelocities;
        private JobHandle currentJobHandle;
        
        private List<AIAgent> agents = new List<AIAgent>();
        
        private void Start()
        {
            InitializeArrays();
            InvokeRepeating(nameof(UpdateAI), 0f, aiUpdateInterval);
        }

        private void InitializeArrays()
        {
            aiPositions = new NativeArray<float3>(maxAIAgents, Allocator.Persistent);
            aiTargets = new NativeArray<float3>(maxAIAgents, Allocator.Persistent);
            aiVelocities = new NativeArray<float3>(maxAIAgents, Allocator.Persistent);
        }

        private void UpdateAI()
        {
            // Update native arrays with current positions
            for (int i = 0; i < agents.Count && i < maxAIAgents; i++)
            {
                aiPositions[i] = agents[i].transform.position;
                aiTargets[i] = agents[i].GetTarget();
            }
            
            // Schedule pathfinding job
            AIPathfindingJob job = new AIPathfindingJob
            {
                positions = aiPositions,
                targets = aiTargets,
                velocities = aiVelocities,
                deltaTime = aiUpdateInterval,
                moveSpeed = 5f
            };
            
            currentJobHandle = job.Schedule(agents.Count, 32);
        }

        private void LateUpdate()
        {
            // Complete job and apply results
            currentJobHandle.Complete();
            
            for (int i = 0; i < agents.Count && i < maxAIAgents; i++)
            {
                agents[i].ApplyVelocity(aiVelocities[i]);
            }
        }

        private void OnDestroy()
        {
            currentJobHandle.Complete();
            
            if (aiPositions.IsCreated) aiPositions.Dispose();
            if (aiTargets.IsCreated) aiTargets.Dispose();
            if (aiVelocities.IsCreated) aiVelocities.Dispose();
        }

        public void RegisterAgent(AIAgent agent)
        {
            if (agents.Count < maxAIAgents)
            {
                agents.Add(agent);
            }
        }

        public void UnregisterAgent(AIAgent agent)
        {
            agents.Remove(agent);
        }
    }

    // Procedural Generation System
    public class ProceduralWorldGenerator : MonoBehaviour
    {
        [Header("World Settings")]
        [SerializeField] private int worldWidth = 100;
        [SerializeField] private int worldHeight = 100;
        [SerializeField] private float noiseScale = 20f;
        [SerializeField] private int octaves = 4;
        [SerializeField] private float persistence = 0.5f;
        [SerializeField] private float lacunarity = 2f;
        
        [Header("Biomes")]
        [SerializeField] private BiomeSettings[] biomes;
        
        [Header("Objects")]
        [SerializeField] private GameObject[] treePrefabs;
        [SerializeField] private GameObject[] rockPrefabs;
        [SerializeField] private GameObject[] grassPrefabs;
        
        private float[,] heightMap;
        private int[,] biomeMap;
        private MeshFilter meshFilter;
        private MeshCollider meshCollider;

        [System.Serializable]
        public class BiomeSettings
        {
            public string name;
            public float minHeight;
            public float maxHeight;
            public Color color;
            public GameObject[] decorations;
            public float decorationDensity;
        }

        private void Start()
        {
            GenerateWorld();
        }

        public void GenerateWorld()
        {
            // Generate height map
            heightMap = GenerateHeightMap();
            
            // Generate biome map
            biomeMap = GenerateBiomeMap(heightMap);
            
            // Create terrain mesh
            Mesh terrainMesh = GenerateTerrainMesh(heightMap);
            ApplyMesh(terrainMesh);
            
            // Place decorations
            PlaceDecorations();
            
            // Generate rivers
            GenerateRivers();
            
            // Place structures
            PlaceStructures();
        }

        private float[,] GenerateHeightMap()
        {
            float[,] map = new float[worldWidth, worldHeight];
            
            System.Random prng = new System.Random(gameConfig.worldSeed);
            Vector2[] octaveOffsets = new Vector2[octaves];
            
            for (int i = 0; i < octaves; i++)
            {
                float offsetX = prng.Next(-100000, 100000);
                float offsetY = prng.Next(-100000, 100000);
                octaveOffsets[i] = new Vector2(offsetX, offsetY);
            }
            
            float maxNoiseHeight = float.MinValue;
            float minNoiseHeight = float.MaxValue;
            
            for (int y = 0; y < worldHeight; y++)
            {
                for (int x = 0; x < worldWidth; x++)
                {
                    float amplitude = 1;
                    float frequency = 1;
                    float noiseHeight = 0;
                    
                    for (int i = 0; i < octaves; i++)
                    {
                        float sampleX = (x - worldWidth / 2f) / noiseScale * frequency + octaveOffsets[i].x;
                        float sampleY = (y - worldHeight / 2f) / noiseScale * frequency + octaveOffsets[i].y;
                        
                        float perlinValue = Mathf.PerlinNoise(sampleX, sampleY) * 2 - 1;
                        noiseHeight += perlinValue * amplitude;
                        
                        amplitude *= persistence;
                        frequency *= lacunarity;
                    }
                    
                    if (noiseHeight > maxNoiseHeight) maxNoiseHeight = noiseHeight;
                    if (noiseHeight < minNoiseHeight) minNoiseHeight = noiseHeight;
                    
                    map[x, y] = noiseHeight;
                }
            }
            
            // Normalize height map
            for (int y = 0; y < worldHeight; y++)
            {
                for (int x = 0; x < worldWidth; x++)
                {
                    map[x, y] = Mathf.InverseLerp(minNoiseHeight, maxNoiseHeight, map[x, y]);
                }
            }
            
            return map;
        }

        private int[,] GenerateBiomeMap(float[,] heightMap)
        {
            int[,] biomeMap = new int[worldWidth, worldHeight];
            
            for (int y = 0; y < worldHeight; y++)
            {
                for (int x = 0; x < worldWidth; x++)
                {
                    float height = heightMap[x, y];
                    
                    for (int i = 0; i < biomes.Length; i++)
                    {
                        if (height >= biomes[i].minHeight && height <= biomes[i].maxHeight)
                        {
                            biomeMap[x, y] = i;
                            break;
                        }
                    }
                }
            }
            
            return biomeMap;
        }

        private Mesh GenerateTerrainMesh(float[,] heightMap)
        {
            Mesh mesh = new Mesh();
            mesh.name = "Procedural Terrain";
            
            Vector3[] vertices = new Vector3[worldWidth * worldHeight];
            int[] triangles = new int[(worldWidth - 1) * (worldHeight - 1) * 6];
            Vector2[] uvs = new Vector2[vertices.Length];
            Color[] colors = new Color[vertices.Length];
            
            int vertIndex = 0;
            int triIndex = 0;
            
            for (int y = 0; y < worldHeight; y++)
            {
                for (int x = 0; x < worldWidth; x++)
                {
                    float height = heightMap[x, y] * 10f; // Scale height
                    vertices[vertIndex] = new Vector3(x, height, y);
                    uvs[vertIndex] = new Vector2((float)x / worldWidth, (float)y / worldHeight);
                    
                    // Set vertex color based on biome
                    int biomeIndex = biomeMap[x, y];
                    colors[vertIndex] = biomes[biomeIndex].color;
                    
                    // Create triangles
                    if (x < worldWidth - 1 && y < worldHeight - 1)
                    {
                        triangles[triIndex] = vertIndex;
                        triangles[triIndex + 1] = vertIndex + worldWidth + 1;
                        triangles[triIndex + 2] = vertIndex + worldWidth;
                        
                        triangles[triIndex + 3] = vertIndex;
                        triangles[triIndex + 4] = vertIndex + 1;
                        triangles[triIndex + 5] = vertIndex + worldWidth + 1;
                        
                        triIndex += 6;
                    }
                    
                    vertIndex++;
                }
            }
            
            mesh.vertices = vertices;
            mesh.triangles = triangles;
            mesh.uv = uvs;
            mesh.colors = colors;
            mesh.RecalculateNormals();
            mesh.RecalculateBounds();
            
            return mesh;
        }

        private void ApplyMesh(Mesh mesh)
        {
            if (meshFilter == null)
                meshFilter = GetComponent<MeshFilter>() ?? gameObject.AddComponent<MeshFilter>();
            
            if (meshCollider == null)
                meshCollider = GetComponent<MeshCollider>() ?? gameObject.AddComponent<MeshCollider>();
            
            meshFilter.mesh = mesh;
            meshCollider.sharedMesh = mesh;
        }

        private void PlaceDecorations()
        {
            System.Random prng = new System.Random(gameConfig.worldSeed + 1);
            
            for (int y = 0; y < worldHeight; y += 2)
            {
                for (int x = 0; x < worldWidth; x += 2)
                {
                    int biomeIndex = biomeMap[x, y];
                    BiomeSettings biome = biomes[biomeIndex];
                    
                    if (prng.NextDouble() < biome.decorationDensity)
                    {
                        GameObject decoration = biome.decorations[prng.Next(biome.decorations.Length)];
                        float height = heightMap[x, y] * 10f;
                        Vector3 position = new Vector3(x, height, y);
                        
                        GameObject instance = Instantiate(decoration, position, Quaternion.identity);
                        
                        // Random rotation and scale
                        instance.transform.rotation = Quaternion.Euler(0, prng.Next(360), 0);
                        float scale = (float)(0.8 + prng.NextDouble() * 0.4);
                        instance.transform.localScale = Vector3.one * scale;
                    }
                }
            }
        }

        private void GenerateRivers()
        {
            // Implement river generation using flow field
        }

        private void PlaceStructures()
        {
            // Implement structure placement (villages, dungeons, etc.)
        }
    }

    // Shader and Graphics
    public class ShaderController : MonoBehaviour
    {
        [Header("Post-Processing")]
        [SerializeField] private Material postProcessMaterial;
        [SerializeField] private float bloomIntensity = 1f;
        [SerializeField] private float vignetteIntensity = 0.3f;
        
        [Header("Dynamic Lighting")]
        [SerializeField] private Light sunLight;
        [SerializeField] private Gradient sunColor;
        [SerializeField] private AnimationCurve sunIntensity;
        [SerializeField] private float dayDuration = 300f; // 5 minutes
        
        private float currentTimeOfDay = 0.5f; // 0 = midnight, 0.5 = noon, 1 = midnight

        private void Start()
        {
            // Set up shader properties
            Shader.SetGlobalFloat("_GlobalWindStrength", 1f);
            Shader.SetGlobalVector("_GlobalWindDirection", new Vector4(1, 0, 0, 0));
        }

        private void Update()
        {
            UpdateTimeOfDay();
            UpdateLighting();
            UpdateShaderGlobals();
        }

        private void UpdateTimeOfDay()
        {
            currentTimeOfDay += Time.deltaTime / dayDuration;
            if (currentTimeOfDay >= 1f) currentTimeOfDay -= 1f;
        }

        private void UpdateLighting()
        {
            // Update sun rotation
            float sunAngle = currentTimeOfDay * 360f - 90f;
            sunLight.transform.rotation = Quaternion.Euler(sunAngle, 30f, 0f);
            
            // Update sun color and intensity
            sunLight.color = sunColor.Evaluate(currentTimeOfDay);
            sunLight.intensity = sunIntensity.Evaluate(currentTimeOfDay);
            
            // Update fog
            RenderSettings.fogColor = Color.Lerp(
                sunColor.Evaluate(currentTimeOfDay),
                Color.gray,
                0.5f
            );
        }

        private void UpdateShaderGlobals()
        {
            // Wind animation
            float windTime = Time.time * 0.5f;
            Shader.SetGlobalFloat("_GlobalWindTime", windTime);
            
            // Water animation
            Shader.SetGlobalFloat("_WaterWaveHeight", 0.5f);
            Shader.SetGlobalFloat("_WaterWaveSpeed", 1f);
            
            // Season effects
            float seasonValue = Mathf.Sin(Time.time * 0.01f) * 0.5f + 0.5f;
            Shader.SetGlobalFloat("_SeasonBlend", seasonValue);
        }

        private void OnRenderImage(RenderTexture source, RenderTexture destination)
        {
            if (postProcessMaterial != null)
            {
                postProcessMaterial.SetFloat("_BloomIntensity", bloomIntensity);
                postProcessMaterial.SetFloat("_VignetteIntensity", vignetteIntensity);
                Graphics.Blit(source, destination, postProcessMaterial);
            }
            else
            {
                Graphics.Blit(source, destination);
            }
        }
    }

    // Supporting Classes and Interfaces
    public interface IDamageable
    {
        void TakeDamage(float amount, Vector3 hitPoint);
        void Heal(float amount);
        float GetCurrentHealth();
        float GetMaxHealth();
    }

    public interface IInteractable
    {
        void Interact(GameObject interactor);
        bool CanInteract(GameObject interactor);
        string GetInteractionPrompt();
    }

    public interface IPickupable
    {
        void Pickup(GameObject picker);
        void Drop(Vector3 position);
        ItemData GetItemData();
    }

    [System.Serializable]
    public class GameConfig : ScriptableObject
    {
        public bool isMultiplayer = false;
        public GameObject playerPrefab;
        public Vector3 playerSpawnPoint;
        public NetworkTransport networkTransport;
        public int worldSeed = 12345;
        public float gameDuration = 600f; // 10 minutes
    }

    [System.Serializable]
    public class ItemData
    {
        public string itemName;
        public Sprite icon;
        public int stackSize = 1;
        public ItemType type;
        public float weight;
        public int value;
        public Dictionary<string, float> stats;
    }

    public enum ItemType
    {
        Weapon,
        Armor,
        Consumable,
        Resource,
        Quest,
        Currency
    }

    public enum InputType
    {
        Move,
        Jump,
        Attack,
        Dash,
        Interact,
        Inventory
    }

    public enum AttackInput
    {
        Light,
        Heavy,
        Special,
        Block,
        Parry
    }

    public struct InputCommand
    {
        public InputType type;
        public Vector3 moveDirection;
        public Vector3 dashDirection;
        public float timestamp;
    }

    public enum InputMode
    {
        Gameplay,
        Menu,
        Cutscene,
        Disabled
    }

    // Placeholder classes (would be implemented separately)
    public class SaveSystem { }
    public class InputManager : MonoBehaviour 
    {
        public static InputManager Instance;
        public Action<Vector2> OnMoveInput;
        public Action OnJumpInput;
        public Action<Vector3> OnDashInput;
        public void SetInputMode(InputMode mode) { }
    }
    public class AudioManager : MonoBehaviour 
    {
        public void PlayMusic(string name) { }
        public void PlaySFX(string name) { }
        public void PlaySFX(AudioClip clip) { }
    }
    public class PoolManager : MonoBehaviour 
    {
        public T GetFromPool<T>(string poolName) where T : Component { return null; }
    }
    public class AIAgent : MonoBehaviour 
    {
        public Vector3 GetTarget() { return Vector3.zero; }
        public void ApplyVelocity(float3 velocity) { }
    }
}
```

## Example 2

```cpp
// GameFramework.h - Unreal Engine 5 Core Framework
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/Character.h"
#include "Components/ActorComponent.h"
#include "Engine/DataAsset.h"
#include "Net/UnrealNetwork.h"
#include "GameFramework.generated.h"

// Game State Management
UENUM(BlueprintType)
enum class EGameState : uint8
{
    MainMenu    UMETA(DisplayName = "Main Menu"),
    Loading     UMETA(DisplayName = "Loading"),
    Playing     UMETA(DisplayName = "Playing"),
    Paused      UMETA(DisplayName = "Paused"),
    GameOver    UMETA(DisplayName = "Game Over"),
    Victory     UMETA(DisplayName = "Victory")
};

// Advanced Game Mode
UCLASS()
class GAMENAME_API AAdvancedGameMode : public AGameModeBase
{
    GENERATED_BODY()

protected:
    UPROPERTY(BlueprintReadOnly, Category = "Game State")
    EGameState CurrentGameState;

    UPROPERTY(EditDefaultsOnly, Category = "Game Config")
    class UGameConfiguration* GameConfig;

    UPROPERTY()
    TMap<FString, UObject*> GameData;

public:
    AAdvancedGameMode();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

    UFUNCTION(BlueprintCallable, Category = "Game State")
    void ChangeGameState(EGameState NewState);

    UFUNCTION(BlueprintImplementableEvent, Category = "Game State")
    void OnGameStateChanged(EGameState NewState);

    UFUNCTION(Server, Reliable, WithValidation)
    void ServerChangeGameState(EGameState NewState);

    UFUNCTION(NetMulticast, Reliable)
    void MulticastGameStateChanged(EGameState NewState);

    UFUNCTION(BlueprintCallable, Category = "Game Data")
    void SaveGameData(const FString& Key, UObject* Value);

    UFUNCTION(BlueprintCallable, Category = "Game Data")
    UObject* LoadGameData(const FString& Key);

protected:
    virtual void HandleMatchIsWaitingToStart() override;
    virtual void HandleMatchHasStarted() override;
    virtual void HandleMatchHasEnded() override;

private:
    void EnterState(EGameState State);
    void ExitState(EGameState State);
    void InitializeGameSystems();
    void ShutdownGameSystems();
};

// Advanced Character with Enhanced Movement
UCLASS()
class GAMENAME_API AAdvancedCharacter : public ACharacter
{
    GENERATED_BODY()

protected:
    // Movement Properties
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Movement")
    float WalkSpeed = 600.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Movement")
    float SprintSpeed = 900.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Movement")
    float CrouchSpeed = 300.0f;

    // Advanced Movement
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Advanced Movement")
    float WallRunSpeed = 700.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Advanced Movement")
    float WallJumpForce = 800.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Advanced Movement")
    float DashDistance = 500.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Advanced Movement")
    float DashCooldown = 1.0f;

    // State Variables
    UPROPERTY(BlueprintReadOnly, Replicated)
    bool bIsWallRunning;

    UPROPERTY(BlueprintReadOnly, Replicated)
    bool bIsSliding;

    UPROPERTY(BlueprintReadOnly, Replicated)
    bool bIsMantling;

    UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_Health)
    float Health;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Stats")
    float MaxHealth = 100.0f;

    // Combat Component
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UCombatComponent* CombatComponent;

    // Inventory Component
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UInventoryComponent* InventoryComponent;

public:
    AAdvancedCharacter();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    // Movement Functions
    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StartSprint();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StopSprint();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void PerformDash();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StartWallRun();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StopWallRun();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void PerformWallJump();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StartSlide();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void StopSlide();

    UFUNCTION(BlueprintCallable, Category = "Movement")
    void PerformMantle();

    // Combat Functions
    UFUNCTION(BlueprintCallable, Category = "Combat")
    void PerformAttack();

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void PerformHeavyAttack();

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void StartBlocking();

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void StopBlocking();

    // Damage System
    UFUNCTION(BlueprintCallable, Category = "Health")
    virtual float TakeDamage(float DamageAmount, struct FDamageEvent const& DamageEvent, 
                             class AController* EventInstigator, AActor* DamageCauser) override;

    UFUNCTION(BlueprintCallable, Category = "Health")
    void Heal(float HealAmount);

    UFUNCTION()
    void OnRep_Health();

    // Network Functions
    UFUNCTION(Server, Reliable, WithValidation)
    void ServerPerformDash();

    UFUNCTION(NetMulticast, Reliable)
    void MulticastPlayDashEffect();

protected:
    // Input Handlers
    void MoveForward(float Value);
    void MoveRight(float Value);
    void Turn(float Value);
    void LookUp(float Value);

private:
    float LastDashTime;
    FVector WallRunNormal;
    
    void UpdateWallRunning();
    void CheckForWallRun();
    void UpdateSliding();
    bool CanMantle() const;
    FVector GetMantleLocation() const;
};

// Combat Component
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class GAMENAME_API UCombatComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    float BaseDamage = 20.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    float AttackRange = 200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    float AttackCooldown = 0.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combo")
    TArray<class UComboData*> AvailableCombos;

protected:
    UPROPERTY()
    TArray<EAttackType> CurrentComboSequence;

    float LastAttackTime;
    float ComboWindow = 1.0f;
    int32 ComboCounter = 0;

public:
    UCombatComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, 
                               FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void PerformAttack(EAttackType AttackType);

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void ResetCombo();

    UFUNCTION(BlueprintCallable, Category = "Combat")
    bool CheckComboMatch(class UComboData* Combo);

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void ExecuteCombo(class UComboData* Combo);

protected:
    virtual void BeginPlay() override;

private:
    void ProcessAttack(EAttackType AttackType);
    TArray<AActor*> GetTargetsInRange();
    void ApplyDamageToTargets(const TArray<AActor*>& Targets, float Damage);
};

// Procedural Level Generation
UCLASS()
class GAMENAME_API AProceduralLevelGenerator : public AActor
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Generation")
    int32 WorldWidth = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Generation")
    int32 WorldHeight = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Generation")
    float NoiseScale = 20.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Generation")
    int32 Seed = 12345;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Biomes")
    TArray<class UBiomeData*> Biomes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Objects")
    TArray<TSubclassOf<AActor>> TreeClasses;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Objects")
    TArray<TSubclassOf<AActor>> RockClasses;

protected:
    UPROPERTY()
    class UProceduralMeshComponent* TerrainMesh;

    TArray<float> HeightMap;
    TArray<int32> BiomeMap;

public:
    AProceduralLevelGenerator();

    virtual void BeginPlay() override;

    UFUNCTION(BlueprintCallable, Category = "Generation")
    void GenerateWorld();

    UFUNCTION(BlueprintCallable, Category = "Generation")
    void ClearWorld();

protected:
    void GenerateHeightMap();
    void GenerateBiomeMap();
    void CreateTerrainMesh();
    void PlaceVegetation();
    void GenerateRivers();
    void PlaceStructures();

private:
    float GetNoiseValue(float X, float Y);
    int32 DetermineBiome(float Height, float Moisture);
    FVector GetSpawnLocation(int32 X, int32 Y);
    bool IsValidSpawnLocation(const FVector& Location);
};

// Loot System
USTRUCT(BlueprintType)
struct FLootTableEntry
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSubclassOf<class AItemBase> ItemClass;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DropChance = 0.1f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinQuantity = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxQuantity = 1;
};

UCLASS()
class GAMENAME_API ULootTable : public UDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    TArray<FLootTableEntry> LootEntries;

    UFUNCTION(BlueprintCallable, Category = "Loot")
    TArray<class AItemBase*> GenerateLoot(UWorld* World);
};
```

## Example 3

```gdscript
# GameFramework.gd - Godot 4 Game Framework
extends Node

class_name GameFramework

# Game State Management
enum GameState {
    MAIN_MENU,
    LOADING,
    PLAYING,
    PAUSED,
    GAME_OVER,
    VICTORY
}

var current_state: GameState = GameState.MAIN_MENU
var game_data: Dictionary = {}

signal game_state_changed(new_state)
signal score_changed(score)
signal health_changed(health)

# Singleton Pattern
static var instance: GameFramework

func _ready():
    if instance == null:
        instance = self
        process_mode = Node.PROCESS_MODE_ALWAYS
    else:
        queue_free()

func change_game_state(new_state: GameState) -> void:
    if current_state == new_state:
        return
    
    exit_state(current_state)
    current_state = new_state
    enter_state(new_state)
    emit_signal("game_state_changed", new_state)

func enter_state(state: GameState) -> void:
    match state:
        GameState.MAIN_MENU:
            get_tree().paused = false
            AudioManager.play_music("main_menu")
        GameState.LOADING:
            load_game_resources()
        GameState.PLAYING:
            get_tree().paused = false
            AudioManager.play_music("gameplay")
        GameState.PAUSED:
            get_tree().paused = true
        GameState.GAME_OVER:
            save_high_score()
            show_game_over_ui()

func exit_state(state: GameState) -> void:
    match state:
        GameState.PAUSED:
            get_tree().paused = false

# Advanced Character Controller
class_name AdvancedCharacter
extends CharacterBody3D

@export var walk_speed: float = 5.0
@export var run_speed: float = 10.0
@export var jump_velocity: float = 8.0
@export var dash_distance: float = 5.0
@export var wall_run_speed: float = 7.0

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var is_wall_running: bool = false
var is_sliding: bool = false
var can_dash: bool = true
var wall_normal: Vector3

@onready var camera: Camera3D = $Camera3D
@onready var raycast: RayCast3D = $RayCast3D

func _physics_process(delta: float) -> void:
    handle_movement(delta)
    handle_wall_run(delta)
    handle_combat()
    move_and_slide()

func handle_movement(delta: float) -> void:
    # Add gravity
    if not is_on_floor():
        velocity.y -= gravity * delta
    
    # Handle jump
    if Input.is_action_just_pressed("jump"):
        if is_on_floor():
            velocity.y = jump_velocity
        elif is_wall_running:
            perform_wall_jump()
    
    # Handle dash
    if Input.is_action_just_pressed("dash") and can_dash:
        perform_dash()
    
    # Get input direction
    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
    
    if direction:
        var speed = run_speed if Input.is_action_pressed("sprint") else walk_speed
        velocity.x = direction.x * speed
        velocity.z = direction.z * speed
    else:
        velocity.x = move_toward(velocity.x, 0, walk_speed * delta * 3)
        velocity.z = move_toward(velocity.z, 0, walk_speed * delta * 3)

func handle_wall_run(delta: float) -> void:
    if is_on_wall() and not is_on_floor() and velocity.y > 0:
        start_wall_run()
    elif is_wall_running and (is_on_floor() or not is_on_wall()):
        stop_wall_run()
    
    if is_wall_running:
        velocity.y = lerp(velocity.y, 0.0, delta * 5.0)
        var wall_forward = wall_normal.cross(Vector3.UP)
        velocity = wall_forward * wall_run_speed

func perform_dash() -> void:
    can_dash = false
    var dash_direction = -transform.basis.z * dash_distance
    velocity = dash_direction
    
    # Cooldown timer
    await get_tree().create_timer(1.0).timeout
    can_dash = true

func perform_wall_jump() -> void:
    velocity = wall_normal * 10.0 + Vector3.UP * jump_velocity
    is_wall_running = false

# Combat System
class_name CombatSystem
extends Node

@export var base_damage: float = 10.0
@export var attack_range: float = 2.0
@export var combo_window: float = 1.0

var current_combo: Array = []
var last_attack_time: float = 0.0
var available_combos: Dictionary = {}

signal combo_performed(combo_name)
signal damage_dealt(amount, target)

func _ready():
    load_combos()

func perform_attack(attack_type: String) -> void:
    var current_time = Time.get_ticks_msec() / 1000.0
    
    if current_time - last_attack_time > combo_window:
        current_combo.clear()
    
    current_combo.append(attack_type)
    last_attack_time = current_time
    
    var combo = check_combo()
    if combo:
        execute_combo(combo)
        current_combo.clear()
    else:
        execute_basic_attack(attack_type)

func check_combo() -> Dictionary:
    for combo_name in available_combos:
        var combo = available_combos[combo_name]
        if arrays_equal(current_combo, combo.sequence):
            return combo
    return {}

func execute_combo(combo: Dictionary) -> void:
    emit_signal("combo_performed", combo.name)
    apply_area_damage(combo.damage * 2, combo.range * 1.5)

func execute_basic_attack(attack_type: String) -> void:
    apply_area_damage(base_damage, attack_range)

func apply_area_damage(damage: float, range: float) -> void:
    var space_state = get_world_3d().direct_space_state
    var query = PhysicsShapeQueryParameters3D.new()
    query.shape = SphereShape3D.new()
    query.shape.radius = range
    query.transform.origin = global_position
    
    var results = space_state.intersect_shape(query)
    for result in results:
        var target = result.collider
        if target.has_method("take_damage"):
            target.take_damage(damage)
            emit_signal("damage_dealt", damage, target)

# Procedural Generation
class_name ProceduralWorld
extends Node3D

@export var world_size: Vector2i = Vector2i(100, 100)
@export var noise_scale: float = 20.0
@export var octaves: int = 4
@export var seed_value: int = 12345

var noise: FastNoiseLite
var height_map: Array = []
var biome_map: Array = []

func _ready():
    generate_world()

func generate_world() -> void:
    setup_noise()
    generate_height_map()
    generate_biomes()
    create_terrain()
    place_objects()

func setup_noise() -> void:
    noise = FastNoiseLite.new()
    noise.seed = seed_value
    noise.frequency = 1.0 / noise_scale
    noise.fractal_octaves = octaves

func generate_height_map() -> void:
    height_map = []
    for y in world_size.y:
        var row = []
        for x in world_size.x:
            var height = noise.get_noise_2d(x, y)
            row.append(height)
        height_map.append(row)

func create_terrain() -> void:
    var mesh_instance = MeshInstance3D.new()
    var array_mesh = ArrayMesh.new()
    var arrays = []
    arrays.resize(Mesh.ARRAY_MAX)
    
    var vertices = PackedVector3Array()
    var uvs = PackedVector2Array()
    var normals = PackedVector3Array()
    
    # Generate vertices
    for y in world_size.y:
        for x in world_size.x:
            var height = height_map[y][x] * 10.0
            vertices.push_back(Vector3(x, height, y))
            uvs.push_back(Vector2(float(x) / world_size.x, float(y) / world_size.y))
    
    # Generate triangles and normals
    # ... (triangle generation code)
    
    arrays[Mesh.ARRAY_VERTEX] = vertices
    arrays[Mesh.ARRAY_TEX_UV] = uvs
    arrays[Mesh.ARRAY_NORMAL] = normals
    
    array_mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
    mesh_instance.mesh = array_mesh
    add_child(mesh_instance)
```
